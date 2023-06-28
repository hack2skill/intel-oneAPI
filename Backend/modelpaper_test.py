import openai

prompt = "generate two new question paper by analysing the question papers given below"

data = """BTS-411(15)-11.16-1510 Reg. No.                            D



   B. Tech. Degree III Semester Examination November 2016

                      CS 15-1302 LOGIC DESIGN 
                           (2015 Scheme)
 Time : 3 Hours                                Maximum Marks : 60

                             PART A
                        (Answer ALL questions)      (10 x 2 = 20)

 I.  (a) Convert (63.25) 10 to Hexa decimal and octal.
     (b) State De-Morgans theorem.
     (c) Express the Boolean function F = A+ B'C as a sum of minterms.
     (d) Differentiate between combinational and sequential circuits.
     (e) Design a 4 x 16 decoder constructed two 3 x 8 decoder.
     (f) Implement a full adder using ONE 3 input decoder and gates.
     (g) Write short notes on triggering of flip flops.
     (h) Write a short note on excitation tables.
     (i) Draw the PLA block diagram and explain its features.
     (j) Write the features of CMOS logic devices.
                             PART B                  (4 x 10 = 40)
 II.     Simplify the following Boolean function into (1) sum-of-products form
         and (ii) product-of-sums form F(A,B,C,D)-----E(0,1,2,5,8,9,10).
                             OR
 III.    Prove the theorems of Boolean algebra by using postulates.

 IV.     Explain the design procedure of combinational circuit with an example
         that converts the BCD to Excess-3 code.
                             OR
 V.      Implement the following function using a multiplexer
         F(A,B,C,D)--E(1, 3, 4,11,12,13,14,15)

 VI      Design a 4 bit ripple counter using J1( flip flop.
                             OR
 VII.    Design and explain a 4 bit asynchronous up-down binary counter.

 VIII.   Write short notes on (1) Fan in and Fan out (ii) Propogation delay 
         (iii) Noise margin.
                             OR
 IX.     Compare TTL and CMOS logic families.

                             ***
BTS —11I(S)— 05.17 — 0720 Reg. No.
                                                                                     A


      Tech. Degree III Semester Supplementary Examination
                                     May 2017

                              CS 154302 LOGIC DESIGN
                                     (2015 Scheme)
   e: 3 Hours                                                      Maximum Marks:60
                                       PART A 
                                 (Answer ALL questions)
                                                                           (10 x 2 = 20)
I.   (a) Perform the following number conversions:
           (i) 567 in Octal to Hex
           (ii) 234.54 in decimal to binary.
     (b) Differentiate between canonical and standard forms of Boolean functions.
     (c) What are universal gates? Why are they called so?
     (d) What is carry look-ahead addition? What is the need?
     (e) Explain the design procedure of a combinational circuit.
     (f) Differentiate between synchronous and asynchronous circuits.
     (g) What is master slave flip flop?
     (h) Differentiate between PLA and PAL.
     (i) Write about ROM, PROM, EPROM and EEPROM.
     (j) Define the following terms: Fan out, Propagation delay and Noise margin.

                                       PART B
                                                                           (4 x 10 = 40)
II.        Simplify the following function using Quine McCluskey method.
           F(A,B,C,D)=1(0,2,3,5,7,8,9,10,11,13,15).
                                          OR
           Simplify the following expression using the K-Map method and implement 
           it using logic gates.
           (i) F = ACE + AlCD1E + A'C' DE.
           (ii) d = DE' + D E + AD 'E' .

IV.        Derive the expressions for a 4-bit magnitude comparator and implement it 
           using logic gates.
                                          OR
V.    (a) Design a decimal adder using 4-bit binary parallel adders.
      (b) Design an excess 3 to BCD code converter using a 4-bit binary parallel 
           adder.

VI.        Design a 4-bit Johnson counter. How does it differ from a ring counter? 
                                          OR
VII.       Design a 4-bit binary ripple counter using JK flip flops.

VIII.      Design a RAM consisting of four words of four bits each. Also show the 
           logic diagram of a typical binary cell.
                                          OR
1          Draw and explain the circuit for a TTL gate with Totem pole output driver.
                                          ***
BTS-III(S)-04.18-0784                          Reg. No.


    B. Tech. Degree III Semester Supplementary Examination
                                                                      April 2018

                                                          CS 15 - 1302 LOGIC DESIGN 
                                                                        (2015 Scheme)

Time: 3 Hours                                                                                                                         Maximum Marks: 60

                                                                             PART A 
                                                                (Answer ALL questions)

                                                                                                                                                    (10 x 2 = 20)
    I.         (a) Convert (AB2)16 to octal.
               (b) Evaluate (DA4C) 16 (648)16 using (r - 1)'s complement.
               (c) Find the complement of AB' + C' D' and reduce it to a minimum number of
                        literals.
               (d) Differentiate between canonical and standard forms of Boolean functions.
               (e) Design a 4 x 16 decoder constructed two 3 x 8 decoder.
               (f) Write notes on triggering of flip flops.
               (g) Write a short note on state tables of a sequential circuit.
               (h) Draw the PLA block diagram and explain its features.
               (i) What is meant by Propagation delay?
               (j) Differentiate between RTL and DTL.

                                                                             PART B
                                                                                                                                                    (4 x    10 = 40)
                        Simplify the following expression using the K-Map method and realize 
                        using NOR gates. F(w, x, y, z) m(1, 5, 6, 12 13, 14) + d(2, 4).
                        Prove the theorems of Boolean algebra by using postulates.OR

  IV.                   Simplify the following Boolean function into (i) sum-of-products form and 
                        (ii) product-of-sums form: F(A, B, C, D) = 1(0, 1, 2, 5, 8, 9, 10).
  V.                    Implement the following Boolean function with NAND gates: OR
                        F(x, y, z) (1, 2, 3, 4, 5, 7).

  VI.                   Implement the following function using a multiplexer (Use B as input). 
                         F(A, B, C, D) = 1(0,1, 3, 4, 8, 9,15).
  VII.                  Design a 4 bit binary ripple counter using JK flip flops. OR

VIII.                   Explain the operation of 2 input CMOS NOR gate and CMOS inverter in 
                        detail.
                                                                                  OR
  IX.                   Explain with circuit diagram a typical 2 input TTL NAND gate.
                                                                                  * *
"""



def separate_question_papers(chunk):
    papers = chunk.split('\n\n')
    question_papers = []
    
    for paper in papers:
        if paper.strip() != '':
            question_papers.append(paper.strip())
    
    return question_papers




# Set up OpenAI API credentials
openai.api_key = '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'

# Function to generate a model question paper using ChatGPT
response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt + data
                }
            ]
        )

important_topics = response.choices[0].message.content


print(important_topics)