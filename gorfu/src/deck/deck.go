package deck

import (
    "fmt"
   // "golang.org/x/tour/tree"
    "sync"
    "math/rand"
//    "github.com/emirpasic/gods/sets/hashset"
    "github.com/emirpasic/gods/sets/treeset"
    "github.com/emirpasic/gods/maps/hashmap"
    "time"
    "common"

)



type hashmapIntf interface {
     Put(interface{}, interface{})
     Get(interface{}) (interface{}, bool)
}
type treesetIntf interface {
     Add(... interface{})
     Remove(...interface{})
     Contains(... interface{}) bool
     Size() int
     Clear()

     Iterator() treeset.Iterator
}

type hashsetIntf interface {
     Add(... interface{})
     Remove(...interface{})
     Contains(... interface{}) bool

     Iterator() treeset.Iterator
}

type  Deck struct {
    set treesetIntf
} 

type  StepDeck struct {
    Deck
} 

func NewDeck() Deck {

        var deck *Deck
        deck = &Deck{}
        deck.set = treeset.NewWith(byID)
        return *deck
}

func (d Deck)  GetSet() treesetIntf {
    return d.set;
}

func (d Deck)  AddStep(s Step) {
         d.set.Add(s)
} 

func (d Deck)  AddStepOp(s StepOp) {
         d.set.Add(s)
} 


func (d Deck)  RemoveStep(step_id int) {

          if d.set.Contains(step_id) {
               d.set.Remove(step_id)
          }
} 

type ErrSeqNameExists float64
type ErrSeqLimitExceeded float64

func (e ErrSeqNameExists) Error() string {
        fmt.Println("Error code := %e occurred\n", float64(e))
        s := fmt.Sprint(float64(e))
        return s
} 

func (e ErrSeqLimitExceeded) Error() string {
        fmt.Println("Error code := %e occurred\n", float64(e))
        s := fmt.Sprint(float64(e))
        return s
} 



type SequenceInquisitor struct {
    names hashmapIntf
} 

var instance *SequenceInquisitor
var once sync.Once

type sequence struct {
        name string

        seq_type string
        seq_id int

        mu sync.Mutex
} 

func GetInquisitor() *SequenceInquisitor {
    once.Do(func() {
        instance = &SequenceInquisitor{}
        instance.names = hashmap.New()

    })
    return instance
} 


type idgen interface {

    next_id() int

} 

type RandomSequence struct {

   sequence
   seed int64

   max int64

   uniques treesetIntf

   randm rand.Rand

} 



func newsequence(name string, seq_type string) (sequence, error) {


       seqInquisitor :=  GetInquisitor();

       var _seq *sequence
       var err ErrSeqNameExists
       _, b :=  seqInquisitor.names.Get(name)
       // we dont want name to exist
       if b {
            err = 41
            return *_seq, err
       }

       seqInquisitor.names.Put(name, true)

       var mu2 sync.Mutex
       _seq = &sequence{"hello", "default", 0, mu2}

       err = 0.0
       return *_seq, err
} 

func newRandomSequence(name string, seedval int64, maxval int64) (RandomSequence, error) {


       seqInquisitor :=  GetInquisitor();

       var _rseq *RandomSequence  
       var err ErrSeqNameExists
       // we dont want name to exist
        _, b :=  seqInquisitor.names.Get(name)
        if b {
            err = 41
            return *_rseq, err 
        } 

        seqInquisitor.names.Put(name, true)

        uni2 := treeset.NewWithIntComparator() 
        src := rand.NewSource(seedval)
        randm := *rand.New(src)

       var mu2 sync.Mutex
       _rseq = &RandomSequence{sequence{name, "random", 0, mu2},
                                   seedval,
                                    maxval,
                                     uni2,
                                      randm }

       _rseq.randm.Seed(seedval)


       err = 0.0
       return *_rseq, err
} 

func (seq sequence) next_id() int {

        seq.mu.Lock()

        defer seq.mu.Unlock()

        defer seq.incr() 
        return seq.seq_id

} 

func (seq sequence) incr() {

    seq.seq_id = seq.seq_id + 1

}

func (seq RandomSequence) next_id() (int, error) {

        seq.mu.Lock()
        defer seq.mu.Unlock()

        for {

          _, noerr := instance.names.Get(seq.name)
          if noerr {
               var err  ErrSeqLimitExceeded
               if int64(seq.uniques.Size()) >= seq.max  {
                   err = 71
                   return 0, err
               }
           
               num := seq.randm.Intn(int(seq.max))

               err = 0.0
               if !seq.uniques.Contains(num) {
                   seq.uniques.Add(num)
                   return num, err
               }
   
          }

        }

}

func (seq sequence) getNames() hashmapIntf  {
     return instance.names
}

func (seq RandomSequence) getNames() hashmapIntf  {
     return instance.names
}

func (seq RandomSequence) reset() {
     seq.uniques = treeset.NewWithIntComparator()
}

func (seq RandomSequence) resetSeed(seedval int64)  {
       seq.uniques = treeset.NewWithIntComparator()
       src := rand.NewSource(seedval)
       seq.randm = *rand.New(src)
}

func (seq sequence)  persist() {

     var durable bool
     if durable {
         go write(seq.seq_id) 
     }
}


func write(qid int) {


}

func (d Deck)  RunTillEnd() {

   fmt.Printf(" Deck.tunTillEnd called. Did you mean StepDeck.runTillEnd()\n");

}

func (deck Deck)  Run() {

      start := time.Now()
      deck.RunTillEnd();
      elapsed := time.Since(start)

      fmt.Printf(" matmul took 5s\n", elapsed);

} 

func (d Deck)  Clear() {
    d.set.Clear();
}

type StepOp interface {

     execute()
     GetId() int
}


type Step struct {

     Name string

     Id int

     Xdim int
     Ydim int

     t1Input *common.T
     t2Param *common.T
     t3Result *common.T

}

func byID(a, b interface{}) int {

     c1 := a.(StepOp)
     c2 := b.(StepOp)


     switch {
         case c1.GetId() > c2.GetId():
             return 1
         case c1.GetId() < c2.GetId():
             return -1
        default:
             return 0
     }



}

func NewStep(name string, id int, xdim int, ydim int) Step {

     var step Step

      step.Name = name
      step.Id = id

      step.Xdim = xdim
      step.Ydim = ydim

      step.t1Input = common.NewT(step.Xdim*step.Ydim)
      step.t2Param = common.NewT(step.Xdim*step.Ydim)
      step.t3Result = common.NewT(step.Xdim*step.Ydim)

     return step

}

func (s Step) GetId() int {
    return s.Id
}



func (s Step) execute() {

}





