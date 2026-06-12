import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ahluwalia Growth OS",
  description: "Business Operating System for Ahluwalia Marbles",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#f5f5f7] text-[#1d1d1f] antialiased">
        {children}
      </body>
    </html>
  );
}
