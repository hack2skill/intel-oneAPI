import React from 'react'
import Lottie from 'lottie-react';
import animation from '../assets/39701-robot-bot-3d.json';
import { Link } from 'react-router-dom';
function Hero() {
  return (
    <div>
    <section className="bg-gradient-to-tr from-violet-700 via-green-600 to-green-400 mt-4 w-screen h-screen">
    <div className="grid max-w-screen-xl px-4 py-8 mx-auto lg:gap-8 xl:gap-0 lg:py-16 lg:grid-cols-12">
        <div className="mr-auto place-self-center lg:col-span-7">
            <h1 className="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl text-white">Unlock Your Academic Potential with LearnMateAI</h1>
            <p className="max-w-2xl mb-6 font-light lg:mb-8 md:text-lg lg:text-xl text-white">Personalized Learning for Smarter Results</p>
            <Link to='/uploadn1'>
            <p className="inline-flex items-center justify-center px-5 py-3 mr-3 text-base font-medium text-center text-white rounded-lg bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 ">
                Get started
                <svg className="w-5 h-5 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd"></path></svg>
            </p>
            </Link>
            {/* <a href="#" className="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-center text-white border border-gray-300 rounded-lg hover:bg-violet-900 focus:ring-4 focus:ring-gray-100  dark:border-gray-700">
                Watch Video
            </a>  */}
        </div>
        <div className="hidden lg:mt-0 lg:col-span-5 lg:flex">
            <Lottie animationData={animation} height={400} width={300}/>    
        </div>                
    </div>
</section>
    </div>
  )
}

export default Hero