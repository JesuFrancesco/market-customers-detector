import { Button } from "@/components/ui/button";
import { useWebcamStream } from "@/hooks/use-webcam";

export default function WebcamViewer() {
  const { frame, skipVideo } = useWebcamStream();

  return (
    <div className="flex flex-col items-center">
      <h2 className="text-xl font-bold mb-2">Cámaras en vivo</h2>
      {frame ? (
        <div className="flex flex-col gap-4">
          <img src={frame} alt="webcam" className="rounded-xl shadow-lg" />
          <Button onClick={skipVideo}>Skip</Button>
        </div>
      ) : (
        <p>Esperando señal de cámaras...</p>
      )}
    </div>
  );
}
