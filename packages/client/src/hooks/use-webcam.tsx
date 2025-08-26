// src/hooks/useWebcamStream.ts
import { useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";

export function useWebcamStream() {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [frame, setFrame] = useState<string | null>(null);

  useEffect(() => {
    const newSocket = io("http://localhost:8000");
    setSocket(newSocket);

    newSocket.on("connect", () => {
      console.log("Connected:", newSocket.id);
    });

    newSocket.on("frame", (data: { image: string }) => {
      setFrame(`data:image/jpeg;base64,${data.image}`);
    });

    newSocket.on("disconnect", () => {
      console.log("Disconnected");
    });

    return () => {
      newSocket.disconnect();
    };
  }, []);

  return { socket, frame };
}
