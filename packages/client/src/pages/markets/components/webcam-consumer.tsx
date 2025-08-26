import { useWebcamStream } from "@/hooks/use-webcam";

export default function WebcamViewer() {
  const { frame } = useWebcamStream();

  return (
    <div className="flex flex-col items-center">
      <h2 className="text-xl font-bold mb-2">Cámaras en vivo</h2>
      {frame ? (
        <img src={frame} alt="webcam" className="rounded-xl shadow-lg" />
      ) : (
        <p>Esperando señal de cámaras...</p>
      )}
    </div>
  );
}
