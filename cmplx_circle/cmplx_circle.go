package main

import (
	"fmt"
	"math"
	"math/cmplx"
	"math/rand"
	"time"
	"image"
	"image/color"
	"image/png"
	"image/draw"
	"os"
)

func init_graph( graph map[string]int) draw.Image {
	img := image.NewRGBA(image.Rectangle{image.Point{0,0},image.Point{graph["w"],graph["h"]}})

	yellow := color.RGBA{ 0xff,0xff ,0x00 ,0xff}

	for x := 0; x < graph["w"]; x++ {
	    for y := 0; y < graph["h"]; y++ {
		switch {
		case 0 == x%graph["sx"] && 0 == y%graph["sy"] : //grid
		    img.Set(x, y, color.White)
		    break
		case x == graph["ax"] || y == graph["ay"] :	//axes
		    img.Set(x, y, yellow)
		    break
		default:					//background
		    img.Set(x, y, color.Black)
		}
	    }
	}
	return img
}

func trace_graph( img draw.Image, graph map[string]int, color color.RGBA ) draw.Image{
	var z complex128
	var x,y float64

	var freq [3]float64
	var norm [3]float64

	rand.Seed(time.Now().UnixNano())
	for i:=0 ; i <len(freq) ; i++ {
		freq[i] = rand.Float64() * rand.Float64() + float64(i)
		if rand.Int() % 2 == 0 {
			freq[i] *= -1.0
		}
		norm[i] = rand.Float64() * (10.0 + rand.Float64())
	}
	fmt.Println(freq,norm)
	prec := 100000000
	p := 0

	go func(x *int) {	//progress bar in Goroutine
		for *x < ma {
			fmt.Print("\r [" , ( *x * 100)/ma , "%] Draw process")
		}
		fmt.Print("\r [END] Draw process")
	}(&p)

	for p = 0; p < prec ; p++ {
		// sigma ( z_n )
		for i:=0 ; i < len(freq) ; i++ {
			z += fonction( float64(p)*freq[i] , norm[i])
		}

		x = real(z)
		y = imag(z)
		img.(draw.Image).Set(  graph["ax"] + int(x*float64(graph["sx"])) , graph["ay"] - int(y*float64(graph["sy"])), color)
	}
	return img
}

func fonction( t float64, c float64 ) complex128 {	//mathematical function
	return complex(c,0)*cmplx.Exp(2i*complex(t,0)*math.Pi*math.Pi)
}

func main() {

	graph := make(map[string]int)
	// sx,sy	size zoom
	graph["sx"] = 60
	graph["sy"] = 60
	// w,h 		width/height
	graph["w"] = 1920*3
	graph["h"] = 1080*3
	// ax,ay	position of axes
	graph["ax"] = graph["w"] / 2
	graph["ay"] = graph["h"] / 2


	img := init_graph( graph )
	img = trace_graph( img , graph, color.RGBA{0xff,0x00,0x00,0xff})
	/*
	img = trace_graph( img , graph, color.RGBA{0x00,0xeb,0x00,0xff})
	img = trace_graph( img , graph, color.RGBA{0x01,0x00,0xeb,0xff})
	img = trace_graph( img , graph, color.RGBA{0xeb,0x00,0xeb,0xff})
	img = trace_graph( img , graph, color.RGBA{0x1c,0xff,0x1c,0xff})
	*/
	// Encode as PNG.
	f, _ := os.Create("image.png")
	png.Encode(f, img)
	fmt.Println("exported")

}
