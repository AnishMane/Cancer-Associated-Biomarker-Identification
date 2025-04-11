
import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { X, Menu, Home, Info, Mail } from "lucide-react";

interface MobileNavProps {
  isOpen: boolean;
  setIsOpen: (isOpen: boolean) => void;
}

const MobileNav: React.FC<MobileNavProps> = ({ isOpen, setIsOpen }) => {
  const location = useLocation();
  
  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <>
      <button
        className="md:hidden"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle menu"
      >
        {isOpen ? (
          <X className="h-6 w-6 text-gray-800 dark:text-white" />
        ) : (
          <Menu className="h-6 w-6 text-gray-800 dark:text-white" />
        )}
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.2 }}
            className="absolute left-0 right-0 top-full z-20 bg-white px-4 py-4 shadow-lg dark:bg-gray-800 md:hidden"
          >
            <div className="flex flex-col space-y-4">
              <Link
                to="/"
                className={`flex items-center space-x-2 px-2 py-2 ${
                  isActive("/")
                    ? "rounded-md bg-gray-100 font-semibold text-biology dark:bg-gray-700"
                    : "text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
                }`}
                onClick={() => setIsOpen(false)}
              >
                <Home className="h-5 w-5" />
                <span>Home</span>
              </Link>
              <Link
                to="/about"
                className={`flex items-center space-x-2 px-2 py-2 ${
                  isActive("/about")
                    ? "rounded-md bg-gray-100 font-semibold text-biology dark:bg-gray-700"
                    : "text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
                }`}
                onClick={() => setIsOpen(false)}
              >
                <Info className="h-5 w-5" />
                <span>About</span>
              </Link>
              <Link
                to="/contact"
                className={`flex items-center space-x-2 px-2 py-2 ${
                  isActive("/contact")
                    ? "rounded-md bg-gray-100 font-semibold text-biology dark:bg-gray-700"
                    : "text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
                }`}
                onClick={() => setIsOpen(false)}
              >
                <Mail className="h-5 w-5" />
                <span>Contact</span>
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default MobileNav;
