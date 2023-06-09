import React from "react";
import Cards from "./Cards";
import styles from "./Find.module.css";

import { Navigation, Pagination, Scrollbar } from "swiper";
import { Swiper, SwiperSlide } from "swiper/react";

import "swiper/css";
import "swiper/css/navigation";

const Find = () => {
  return (
    <div className={styles.find}>
      <div className={styles.heading}>
        <h1>Object Detection For Autonomous Vehicles</h1>
        <div className={styles.text_bg}>
          <p>
            <span>Self driving algorithm with (Intel-ONE Api Base toolkit)</span>
          </p>
        </div>
      </div>

      {/* slider container */}
      <div className={styles.slider_container}>
        {/* navigation automaically is set true */}
        <Swiper
          modules={[Navigation, Pagination, Scrollbar]}
          spaceBetween={10}
          slidesPerView={5}
          navigation
          pagination={{clickable:true}}
          scrollbar={{draggable:true}}
          breakpoints={{
            // when window width is >= 340px
            340: {
              width: 200,
              slidesPerView: 1,
            },
            // when window width is >= 768px
            768: {
              width: 768,
              slidesPerView: 4,
            },
            // when window width is >= 1040px
            1040: {
              width: 1040,
              slidesPerView: 5,
            },
          }}
          onSlideChange={() => console.log("slide change")}
          onSwiper={(swiper) => console.log(swiper)}
        >
          {/* each is something we can navigate thro */}
          <SwiperSlide>
            <Cards
              image="https://production-media.paperswithcode.com/datasets/u18.jpg"
              make="traffic signs"
            />
          </SwiperSlide>
          <SwiperSlide>
            <Cards
              image='https://repository-images.githubusercontent.com/185267361/a19fc900-700d-11e9-8070-d225f73a3657'
              make='pedestrians'
            />
          </SwiperSlide>
          <SwiperSlide>
            <Cards
              image='https://user-images.githubusercontent.com/72157067/156183131-b661ba59-22e5-4c73-b5a9-e0b0855cc68a.jpg'
              make='vehicles'
            />
          </SwiperSlide>
          <SwiperSlide>
            <Cards
              image='https://d3i71xaburhd42.cloudfront.net/ff38f4b6d909e074ad91fb18fc9c89aa684197c3/3-Figure4-1.png'
              make='traffic signals'
            />
          </SwiperSlide>
          <SwiperSlide>
            <Cards
              image='https://www.researchgate.net/publication/344906696/figure/fig1/AS:952328895070208@1604064310610/Hand-gestures-performed-in-this-work.jpg'
              make='hand gesture'
            />
          </SwiperSlide>

          <SwiperSlide>
            <Cards
              image='https://images.unsplash.com/photo-1619682817481-e994891cd1f5?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTZ8fHRveW90YXxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=800&q=60'
              make='Toyota'
            />
          </SwiperSlide>
          <SwiperSlide>
            <Cards
              image='https://images.unsplash.com/photo-1588636142475-a62d56692870?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8OHx8amVlcHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=800&q=60'
              make='Jeep'
            />
          </SwiperSlide>
          <SwiperSlide>
            <Cards
              image='https://images.unsplash.com/photo-1604108415419-6d4bd73a1c2c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTB8fGZvcmR8ZW58MHx8MHx8&auto=format&fit=crop&w=800&q=60'
              make='Ford'
            />
          </SwiperSlide>
          <SwiperSlide>
            <Cards
              image='https://images.unsplash.com/photo-1606016159991-dfe4f2746ad5?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8dGVzbGF8ZW58MHx8MHx8&auto=format&fit=crop&w=800&q=60'
              make='Tesla'
            />
          </SwiperSlide>
          <SwiperSlide>
            <Cards
              image='https://images.unsplash.com/photo-1580274455191-1c62238fa333?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8cG9yc2NoZXxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=800&q=60'
              make='Porsche'
            />
          </SwiperSlide>
        </Swiper>
      </div>
    </div>
  );
};

export default Find;
