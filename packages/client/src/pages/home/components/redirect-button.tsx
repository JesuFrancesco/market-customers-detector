import { Button } from "@/components/ui/button";
import React from "react";

const RedirectButton: React.FC<{
  children: React.ReactNode;
  onClick: () => void;
}> = ({ children, onClick }) => {
  return (
    <Button
      className="flex flex-row items-center align-middle text-2xl"
      variant={"default"}
      onClick={onClick}
    >
      {children}
    </Button>
  );
};

export default RedirectButton;
