// Online Java Compiler
// Use this editor to write, compile and run your Java code online

import java.io.*;


    
    public class LinkedList {
        
    Node head;
    
    static class Node {
    
    int data;
    Node next;
    
    Node(int p_data)
        {
            data=p_data;
            next=null;
        }
    }
    
    public static void insert(LinkedList list,int data)
    {
        Node new_node=new Node(data);
        
        //empty
        if(list.head==null)
        {
            list.head=new_node;
        }
        
        //no empty
        else
        {
            Node last=list.head;
            while(last.next!=null)
            {
                last=last.next;
            }
            last.next=new_node;
            
        }
    }
    
    public static void delete(LinkedList list)
    {
        
        
        //empty
        if(list.head==null)
        {
            System.out.println("Nothing to delete");
        }
        
        Node last=list.head;
        //exactly one
        if(last.next==null)
        {
            list.head=null;
        }
        
        
        //min 2
        else
        {
            
            while(last.next.next!=null)
            {
                last=last.next;
            }
            last.next=null;
            
        }
        
    }
    
    
    public static void deletekey(LinkedList list,int key)
    {
        
        
        //empty
        if(list.head==null)
        {
            System.out.println("Nothing to delete");
        }
        
        Node last=list.head;
        //first one
        if(last.next==null && last.data==key)
        {
            list.head=null;
        }
        
       else{ 
        if(last.data==key)
        {
            list.head=list.head.next;
        }
        last=list.head;
        while(last.next!=null)
            {
                last=last.next;
            }
        //last one
        if(last.data==key)
        {
            delete(list);
        }
        
        
        //min 2
        else
        {last=list.head;
            
            while(last.next!=null)
            {
                if(last.next.data==key)
                {
                    last.next=last.next.next;
                    last.next.next=null;
                }
                last=last.next;
            }
            
            
        }
       }
        
    }
    
    public static void printList(LinkedList list)
    {
        Node current = list.head;
        while(current!=null)
        {
            System.out.print(current.data + " "); 
            current=current.next;
        }
    }
    
    
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        LinkedList list=new LinkedList();
        LinkedList list2=new LinkedList();
        insert(list,1);
        insert(list,2);
        deletekey(list,1);
        deletekey(list,2);
        insert(list,3);
        insert(list,4);
        insert(list,1);
        insert(list,2);
        deletekey(list,1);
        printList(list);
        
    }
}
