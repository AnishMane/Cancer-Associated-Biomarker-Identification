
import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Book, Info, Mail } from "lucide-react";
import MobileNav from "./MobileNav";

const Navbar: React.FC = () => {
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);
  
  const isActive = (path: string) => {
    return location.pathname === path;
  };
  
  return (
    <nav className="sticky top-0 z-10 w-full bg-white shadow-md dark:bg-gray-800">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between py-4">
          {/* Logo/Brand */}
          <Link to="/" className="flex items-center space-x-2">
            <Book className="h-6 w-6 text-biology" />
            <span className="text-xl font-semibold text-gray-800 dark:text-white">OncoTrace.ai</span>
          </Link>
          
          {/* Desktop Navigation Links */}
          <div className="hidden space-x-8 md:flex">
            <Link 
              to="/"
              className={`flex items-center space-x-1 ${
                isActive("/") 
                  ? "text-biology font-semibold" 
                  : "text-gray-600 hover:text-biology dark:text-gray-300 dark:hover:text-biology-light"
              }`}
            >
              <span>Home</span>
            </Link>
            <Link 
              to="/about"
              className={`flex items-center space-x-1 ${
                isActive("/about") 
                  ? "text-biology font-semibold" 
                  : "text-gray-600 hover:text-biology dark:text-gray-300 dark:hover:text-biology-light"
              }`}
            >
              <Info className="h-4 w-4" />
              <span>About</span>
            </Link>
            <Link 
              to="/contact"
              className={`flex items-center space-x-1 ${
                isActive("/contact") 
                  ? "text-biology font-semibold" 
                  : "text-gray-600 hover:text-biology dark:text-gray-300 dark:hover:text-biology-light"
              }`}
            >
              <Mail className="h-4 w-4" />
              <span>Contact</span>
            </Link>
          </div>
          
          {/* Mobile Navigation */}
          <div className="relative md:hidden">
            <MobileNav isOpen={isOpen} setIsOpen={setIsOpen} />
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
