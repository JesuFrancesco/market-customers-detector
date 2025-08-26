import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface ICustomer {
  id: number;
  customer: string;
  invoice: string;
  paymentStatus: string;
  totalAmount: string;
  paymentMethod: string;
}

const customers: ICustomer[] = [
  {
    id: 1,
    customer: "John Doe",
    invoice: "INV001",
    paymentStatus: "Paid",
    totalAmount: "$250.00",
    paymentMethod: "Credit Card",
  },
  {
    id: 2,
    customer: "Jane Smith",
    invoice: "INV002",
    paymentStatus: "Pending",
    totalAmount: "$150.00",
    paymentMethod: "PayPal",
  },
  {
    id: 3,
    customer: "Alice Johnson",
    invoice: "INV003",
    paymentStatus: "Unpaid",
    totalAmount: "$350.00",
    paymentMethod: "Bank Transfer",
  },
  {
    id: 4,
    customer: "Bob Brown",
    invoice: "INV004",
    paymentStatus: "Paid",
    totalAmount: "$450.00",
    paymentMethod: "Credit Card",
  },
  {
    id: 5,
    customer: "Charlie Davis",
    invoice: "INV005",
    paymentStatus: "Paid",
    totalAmount: "$550.00",
    paymentMethod: "PayPal",
  },
  {
    id: 6,
    customer: "Eve White",
    invoice: "INV006",
    paymentStatus: "Pending",
    totalAmount: "$200.00",
    paymentMethod: "Bank Transfer",
  },
  {
    id: 7,
    customer: "Frank Black",
    invoice: "INV007",
    paymentStatus: "Unpaid",
    totalAmount: "$300.00",
    paymentMethod: "Credit Card",
  },
];

export function CustomersTable() {
  return (
    <Table>
      <TableCaption>
        Una tabla con los clientes de la cadena del supermercado.
      </TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead className="w-[100px]">Cliente</TableHead>
          <TableHead>Estado</TableHead>
          <TableHead>Método</TableHead>
          <TableHead className="text-right">Monto</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {customers.map((customer) => (
          <TableRow key={customer.id}>
            <TableCell className="font-medium">{customer.customer}</TableCell>
            <TableCell>{customer.paymentStatus}</TableCell>
            <TableCell>{customer.paymentMethod}</TableCell>
            <TableCell className="text-right">{customer.totalAmount}</TableCell>
          </TableRow>
        ))}
      </TableBody>
      <TableFooter>
        <TableRow>
          <TableCell colSpan={3}>Total</TableCell>
          <TableCell className="text-right">$2,500.00</TableCell>
        </TableRow>
      </TableFooter>
    </Table>
  );
}
