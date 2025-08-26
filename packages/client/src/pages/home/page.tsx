import RedirectButton from "./components/redirect-button";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center gap-8 p-4">
      <h1 className="text-2xl font-bold">Hola de nuevo</h1>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-center">
        <RedirectButton
          onClick={() => {
            navigate("/markets");
          }}
        >
          Ver mercados
        </RedirectButton>
        <RedirectButton
          onClick={() => {
            navigate("/vips");
          }}
        >
          Ver vips
        </RedirectButton>
        <RedirectButton
          onClick={() => {
            navigate("/customers");
          }}
        >
          Ver lista de clientes
        </RedirectButton>
      </section>
    </div>
  );
};

export default HomePage;
