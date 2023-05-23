import React from "react";

function Navbar() {
 
  return (
    <div>
      <nav className="bg-blue-400">
        <div className="w-screen mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <img className="h-8 w-8" src="./logo1.png" alt="Workflow" />
              </div>
              <div className="flex justify-end items-center ml-8">
                <div className="flex items-baseline space-x-4">
                  <a
                    href="#"
                    className="hover:bg-gray-700 text-white px-3 py-2 rounded-md text-sm font-medium"
                  >
                    Features
                  </a>

                  <a
                    href="#"
                    className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                  >
                    Testimonials
                  </a>

                  <a
                    href="#"
                    className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                  >
                    About us
                  </a>

                  <a
                    href="#"
                    className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                  >
                    Team
                  </a>

                  <a
                    href="#"
                    className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium ml-auto"
                  >
                    Login
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

      </nav>

      <header className="bg-white shadow">
        {/* ... */}
      </header>

    </div>
  );
}


export default Navbar;