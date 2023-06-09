package main

import (
           "fmt"
           "math/rand"
           "time"
           "strings"
           "sync"
)

var 	board  [][]string
var 	board_slots  [][]string
var    xo  []byte

var num_slots int = 9

var   c chan int
//var   cpos chan int
var xpos, ypos int

var gameover bool

var gameover_check bool
var slotavl bool


var mu sync.Mutex

var loopctr int = 0

func play(c, quit chan int) {
        rand.Seed(57)
	x, y := 0, 1
          for {
		select {
		case c <- x:
			x, y = y, x

                        if loopctr >= 9 {
                           clear_board();
                           loopctr = 0

                           time.Sleep(50 * time.Millisecond)
                        }

                        for {
		            pos := rand.Intn(9)
                            xpos = pos % 3
                            ypos = int(pos/3);


                               slotavl = false
                      //       fmt.Printf(" xpos ypos = %d, %d\n", xpos, ypos);
                      //       fmt.Printf(" board xpos ypos = %s\n", board[xpos][ypos]);
                            if board_slots[xpos][ypos] == string('_') {
                               slotavl = true;
                               loopctr = loopctr + 1
                               break;
                            }

                       //      fmt.Printf(" xpos not avl. looping...\n");

                        }

                 //       cpos <- xpos

		case <-quit:
			return
		}

         }
}

func clear_board() {

            board_slots = [][]string{
		[]string{"_", "_", "_"},
		[]string{"_", "_", "_"},
		[]string{"_", "_", "_"},
	}

}

func main() {
	// Create a tic-tac-toe board.
            board = [][]string{
		[]string{"_", "_", "_"},
		[]string{"_", "_", "_"},
		[]string{"_", "_", "_"},
	}

            board_slots = [][]string{
		[]string{"_", "_", "_"},
		[]string{"_", "_", "_"},
		[]string{"_", "_", "_"},
	}

         xo = []byte { 'X', 'O' }

        c = make(chan int)
	quit := make(chan int)
	go func() {
		for i := 0; i < 10; i++ {
		     print_board();
                   // fmt.Println(<-c)
		}
	        quit <- 0
	}()
        go check_gameover();
	play(c, quit)

}


func print_board() {

//    select {
//        case xpos =  <-cpos:

             ch := xo[<-c]

        //     fmt.Printf(" %s played\n", string(ch))
             board[xpos][ypos] = string(ch)

 //       default:
 //            {}              
 //    }
}



func check_gameover() bool {

                xx := [][]int {
                                  []int {0},
                                  []int {1},
                                  []int {2},
                      }


        var xwin, owin bool
         var x, y int


        var xcol [3]string
        var yrow [3]string


    //    mu.Lock();

       for {

       //if(loopctr >= 9) {

        //loopctr = 0;

     //   defer mu.Unlock();

        for x=0;x<3;x++ {
            for y=0;y<3;y++ {

                xcol[y] = board[x][y]

            }

                 s1str := strings.Join(xcol[:],"")

                 // fmt.Printf(" s1str = %s\n", s1str);

                if strings.Compare(s1str, "XXX") == 0 {
                     xwin = true
                     gameover = xwin
              //      fmt.Printf(" gameover  xxx win= %s\n", s1str);
                }
               //     fmt.Printf(" gameover 9  ret= %s\n", gameover);

                if strings.Compare(s1str, "OOO") == 0 {
                     owin = true
                     gameover = owin
                 //   fmt.Printf(" gameover  o win= %s\n", s1str);
                }


       }

                //    fmt.Printf(" gameover 8  ret= %s\n", gameover);
        for x=0;x<3;x++ {
            for y=0;y<3;y++ {

                yrow[y] = board[y][x]

            }

                 s1str := strings.Join(yrow[:],"")

                // fmt.Printf(" s1str = %s\n", s1str);

               //     fmt.Printf(" gameover 1  ret= %s\n", gameover);
                if strings.Compare(s1str, "XXX") == 0 {
                     xwin = true
                     gameover = xwin
             //       fmt.Printf(" gameover  xxx win= %s\n", s1str);
                }

                if strings.Compare(s1str, "OOO") == 0 {
                     owin = true
                     gameover = owin
                 //   fmt.Printf(" gameover o win = %s\n", s1str);
                }

       }


              //      fmt.Printf(" gameover 2  ret= %s\n", gameover);


                var bz int = 0
             //   var bx int = 2
                var z int = 0
                var yp int = 0
                for z=0;z<len(xx);z++ {
                   // fwd diag
                   yp = xx[z][0]

                   xcol[z] = board[z][yp]

                   bz = 2 - z
                  // bx = 2 - j

                   yp = xx[bz][0]

                   yrow[z] = board[bz][yp]

                }

                 s1str := strings.Join(xcol[:],"")
                 s2str := strings.Join(yrow[:],"")

                if strings.Compare(s1str, "XXX") == 0 {
                     xwin = true
                     gameover = xwin
                 //   fmt.Printf(" gameover  x win= %s\n", s1str);
                }

               //     fmt.Printf(" gameover 3  ret= %s\n", gameover);
                if strings.Compare(s1str, "OOO") == 0 {
                     owin = true
                     gameover = owin
                //    fmt.Printf(" gameover  o win= %s\n", s1str);
                }

           //         fmt.Printf(" gameover 4  ret= %s\n", gameover);
                if strings.Compare(s2str, "OOO") == 0 {
                    owin = true
                     gameover = owin
                 //   fmt.Printf(" gameover  o win= %s\n", s1str);
                }

                if strings.Compare(s2str, "XXX") == 0 {
                    xwin = true
                     gameover = xwin
                 //   fmt.Printf(" gameover  x win= %s\n", s1str);
                }


            //        fmt.Printf(" gameover 5  ret= %s\n", gameover);
        print_game()

        gameover_check = false;


//      }

             //       fmt.Printf(" gameover  ret= %s\n", gameover);


    }

        return gameover

}

func print_header() {

}

func print_header1() {

}

func print_header1() {

}

func print_game() {
         var h,d int
         for h=0;h<3;h++ {
           for d=0;d<3;d++ {
              fmt.Printf("%s", board[h][d])
              fmt.Printf(", ")
           }
          fmt.Printf("\n")
         }

          fmt.Printf("\n")
          fmt.Printf("\n")
          fmt.Printf("\n")

}
