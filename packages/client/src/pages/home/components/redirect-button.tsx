import { Button } from "@/components/ui/button";
import React from "react";

const RedirectButton: React.FC<{
  children: React.ReactNode;
  onClick: () => void;
}> = ({ children, onClick }) => {
  return (
    <Button className="text-2xl" variant={"outline"} onClick={onClick}>
      {children}
    </Button>
  );
};

export default RedirectButton;
