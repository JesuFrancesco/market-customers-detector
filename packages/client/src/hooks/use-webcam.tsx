import { useCallback, useEffect, useState } from "react";
import { io, Socket } from "socket.io-client";

export function useWebcamStream(sioAddress: string) {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [frame, setFrame] = useState<string | null>(null);

  useEffect(() => {
    const newSocket = io(sioAddress, {
      path: "/sio",
    });
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

  const skipVideo = useCallback(() => {
    if (socket) {
      socket.emit("control", { action: "skip" });
      console.log("Sent skip event");
    }
  }, [socket]);

  return { socket, frame, skipVideo };
}
