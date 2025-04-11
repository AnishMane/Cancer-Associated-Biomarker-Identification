
import React from "react";
import Navbar from "./Navbar";
import Footer from "./Footer";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex min-h-screen flex-col bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <Navbar />
      <main className="flex-grow">{children}</main>
      <Footer />
    </div>
  );
};

export default Layout;
