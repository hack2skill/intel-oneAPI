var selector = document.getElementById("selector");
var Name = document.getElementById("name_data");
var DispName = document.getElementById("pet-name");
var pet = document.getElementById("pet");
var food_container = document.getElementById("item-container");
var bar_max_width = document.getElementById('level').offsetWidth - 8;
var bar_height = document.getElementById('info').offsetHeight;
var bar = document.getElementById('bar');
bar.style.height =  `${bar_height}px`;
var display_per = document.getElementById('per');
var percent = parseFloat(display_per.innerHTML); // database     add level too                                                                                           
var grow_width = bar_max_width * percent * 0.01;
var level_desc = document.getElementById("levamt");
var level_amt = parseInt(level_desc.innerHTML);
bar.style.width =  `${grow_width}px`;
var levelplus = document.getElementById("info");
var coins = document.getElementById('coin-amt');

// fetch the pet name and type from the views return if not set yet put pet_type = "" else assign the values
// also fetch the level and level progress and assign those too
// after updating the level and level progress send update request to server where it will update the values to backend virtual pet and give complete code of views

var pet_type_list = ["Dog", "Cat"]

var pet_type = "";
// Function to update the pet details in the UI
function updatePetDetails(petType, petName, level, progress, coindb) {
    // Assign the values to the corresponding variables
    pet_type = petType;
    level_amt = level;
    percent = progress;
  
    // Update the UI with the new values
    DispName.innerHTML = petName;
    level_desc.innerHTML = `${level_amt}`;
    display_per.innerHTML = `${percent}%`;
    coins.innerHTML = `${coindb}`;
  
    // Calculate the growth width for the progress bar
    grow_width = bar_max_width * percent * 0.01;
    bar.style.width = `${grow_width}px`;
  
    // Update the pet image and animation based on the pet type
    if (pet_type === "Dog" || pet_type === "Cat") {
      pet.style.backgroundImage = `url('../static/content/${pet_type}/${pet_type}-Idle.png')`;
      pet.style.animation = "idle 1s steps(8) infinite";
    }
}

// Function to send the updated pet details to the server
function savePetDetails(petName, petType, level, progress, c) {
    // Prepare the data to be sent in the request body
    const data = {
      name: petName,
      type: petType,
      level: level,
      progress: progress,
      coin: c
    };
  
   // Send an AJAX request to the server to save the data
  $.ajax({
    url: '',
    type: 'POST',
    dataType: 'json',
    data: data,
    success: function(response) {
      console.log('Pet details saved successfully');
    },
    error: function(error) {
      console.log('Error saving pet details:', error);
    }
  });
  }

var temp = setInterval(function() {
        if (pet_type !== "Dog" && pet_type !== "Cat") {
            var Dog = document.getElementById("pet-dog");
            var Cat = document.getElementById("pet-cat");
            Dog.addEventListener('click', () => {
                Dog.style.border = "8px solid lime";
                Cat.style.border = "none";
            })
            Cat.addEventListener('click', () => {
                Dog.style.border = "none";
                Cat.style.border = "8px solid lime";
            })
            selector.style.display = 'flex';
            var sel = -1;
        }
        else {
            // updatePetDetails(petType, petName, level, progress, coindb);
            selector.style.display = 'none';
            pet.style.backgroundImage = `url('../static/content/${pet_type}/${pet_type}-Idle.png')`;
            pet.style.animation = "idle 1s steps(8) infinite";
            clearInterval(temp);
        }
    }, Infinity);

    var cost = [0, 20, 20, 30, 10, 10, 20, 30, 30, 50, 20, 70, 20, 30, 10, 10, 20, 20, 60, 80, 80, 30, 20, 70, 80, 60, 60, 50, 40, 20, 10, 30, 20, 50, 70, 70, 60, 20, 40, 40, 60, 60, 80, 80, 30, 20];

    for (let i = 1; i <= 45; i++) {
        food_container.innerHTML += `<button class='feed' onclick=updateLevel(${cost[i]})><img src=../static/content/food/${i}.png /></button><p id='label'><span>${cost[i]}</span><img src='../static/content/coins.png' /></p>`;
    }

    function validate() {
        var radio = document.getElementsByName("sel");
        if (!radio[0].checked && !radio[1].checked) {
            alert("Please select pet type");
        }
        else if (radio[0].checked) {
            sel = 0;
        }
        else {
            sel = 1;
        }
        if (Name.value.trim() === "" && sel !== -1) {
            alert("Please enter your pet name");
        }
        else {
            petName = `${Name.value.trim()}`;
            DispName.innerHTML = petName;
            pet_type = pet_type_list[sel];
            petType = pet_type_list[sel];
            // savePetDetails(petName, petType, level, progress, coindb);
        }
    }

    function updateLevel(addPercent) {
        // adding database connection to fetch last known level and percent
        // temporarily taking current level and percent, remove this later (level_amt => currentLevel) (percent => currentLevel) 
        var coins_left = coins.innerHTML;
        if (coins_left >= addPercent) {
            var feed_buttons = document.querySelectorAll(".feed");
            for (let i = 0; i < feed_buttons.length; i++) {
                feed_buttons[i].disabled = true;  
            }  
            var init_coin = coins_left;
            var coin_spent = setInterval(function() {
                if (coins_left !== init_coin - addPercent) {
                    coins_left--;
                    coins.innerHTML = `${coins_left}`;
                }
                else {
                    for (let i = 0; i < feed_buttons.length; i++) {
                        feed_buttons[i].disabled = false;  
                    }  
                    clearInterval(coin_spent);
                }
            }, 50);
            pet.style.backgroundImage = `url(../static/content/${pet_type}/${pet_type}-Jump.png)`;
            pet.style.animation = "reward 1s steps(8) infinite";
            levelplus.innerHTML = `+${addPercent} Level`;
            levelplus.style.animation = "levelplus 1s infinite";
            var new_percent = percent + addPercent; 
            var temp = percent;
            var interval = setInterval(function () {
                if (temp !== new_percent) { // switch here
                    if (percent + 1 > 100) {
                        percent = 1;
                        level_amt++;
                        level_desc.innerHTML = `${level_amt}`;
                    }
                    else {
                        percent++;
                    }
                    grow_width = bar_max_width * percent * 0.01;
                    level_desc.innerHTML = `${level_amt}`;
                    display_per.innerHTML = `${percent}%`;
                    bar.style.width =  `${grow_width}px`;  
                    temp++; 
                }
                else {
                    clearInterval(interval);
                    var animation = setInterval(function() {
                        levelplus.style.animation = "none";
                        pet.style.backgroundImage = `url(../static/content/${pet_type}/${pet_type}-Idle.png)`;
                        pet.style.animation = "idle 1s steps(8) infinite";
                        clearInterval(animation);
                    }, 800);
                }
            }, 2);
            savePetDetails(petName, petType, level_amt, percent, coins_left);
        } else {
            alert("Error: Not Sufficient Balance!");
        }
    }

    function changeAnimation() {
        if (pet_type === "Dog" || pet_type === "Cat") {
            var action_list = ['idle', 'walk'];
            var action = action_list[Math.floor((Math.random() * action_list.length))];
            if (action === 'idle') {
                pet.style.backgroundImage = `url('../static/content/${pet_type}/${pet_type}-Idle.png')`;
                pet.style.animation = "idle 1s steps(8) infinite";
            }
            else {
                pet.style.backgroundImage = `url('../static/content/${pet_type}/${pet_type}-Walk.png')`;
                pet.style.animation = "walk 3s steps(8) infinite";
            }
        }
    }

    setInterval(changeAnimation, 3000);




