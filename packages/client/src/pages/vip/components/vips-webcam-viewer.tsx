import { Button } from "@/components/ui/button";
import { useWebcamStream } from "@/hooks/use-webcam";

export default function VipsWebcamViewer() {
  const { frame, skipVideo } = useWebcamStream("http://localhost:9000");

  return (
    <div className="flex flex-col items-center">
      <h2 className="text-xl font-bold mb-2">Cámaras vip en vivo</h2>
      {frame ? (
        <div className="flex flex-col items-center gap-4">
          <img src={frame} alt="webcam" className="rounded-xl shadow-lg" />
          <Button className="hover:cursor-pointer w-min" onClick={skipVideo}>
            Cambiar cámara
          </Button>
        </div>
      ) : (
        <p>Esperando señal de cámaras...</p>
      )}
    </div>
  );
}
