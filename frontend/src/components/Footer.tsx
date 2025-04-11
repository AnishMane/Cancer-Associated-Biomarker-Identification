
import React from "react";
import { Github } from "lucide-react";

const Footer: React.FC = () => {
  return (
    <footer className="bg-white py-6 shadow-inner dark:bg-gray-800">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            © {new Date().getFullYear()} OncoTrace.ai. All rights reserved.
          </p>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-1 text-sm text-gray-600 transition-colors hover:text-biology dark:text-gray-400 dark:hover:text-biology-light"
          >
            <Github className="h-4 w-4" />
            <span>GitHub Repository</span>
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
