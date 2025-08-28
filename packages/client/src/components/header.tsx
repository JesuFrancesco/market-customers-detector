import logo from "@/assets/logo.png";
const Header = () => {
  return (
    <header className="flex items-center justify-evenly">
      {/* Logo */}
      <a className="flex items-center gap-x-2 hover:cursor-pointer" href="#">
        <img src={logo} alt="Logo" className="h-12" />
        <h1 className="text-2xl font-bold">Supermercados Lima</h1>
      </a>

      {/* NavBar */}
      <nav>
        <ul className="flex space-x-4">
          <li>
            <a href="#" className="text-blue-500">
              Home
            </a>
          </li>
          {["vips", "markets", "customers"].map((item) => (
            <li key={item}>
              <a href={`#/${item}`} className="text-blue-500">
                {item.charAt(0).toUpperCase() + item.slice(1)}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
};

export default Header;
