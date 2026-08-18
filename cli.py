import quickfix44 as fix44
import quickfix as fix
import uuid


class Cli:
    def __init__(self, running, connected):
        self.running = running
        self.connected = connected

    def prompt_message(self):
        while self.running.is_set() and self.connected.is_set():
            user_prompt = input("fixcli> ")
            user_prompt = user_prompt.strip()

            if not user_prompt:
                print("[App]: invalid command. try again.")
                continue

            split_prompt = user_prompt.split()
            parsed, ok = self.parse_command(split_prompt)

            if ok:
                return parsed

    def parse_command(self, user_prompt):
        command = user_prompt[0]
        args = user_prompt[1:]

        match command:
            case "exit" | "quit":
                self.running.clear()
                return None, True
            case "help":
                self.print_help()
                return None, False
            case "raw":
                return "".join(command), True
            case "new":
                if len(args) != 5:
                    print(
                        "[App]: wrong arg count for new. Usage: new clOrdId symbol side qty price"
                    )
                    return None, False

                return self.msg_builder("new", args), True
            case "exec":
                if len(args) != 6:
                    print(
                        "[App]: wrong arg count for ExecutionReport. Usage: exec OrdId clOrdId symbol side qty price"
                    )
                    return None, False

                return self.msg_builder("exec", args), True
            case _:
                print("[App]: unknown command.")
                self.print_help()
                return None, False

    def msg_builder(self, msg_type, args):
        match msg_type:
            case "new":
                msg = OrderFactory.new_limit_order(
                    str(args[0]),
                    str(args[1]),
                    fix.Side_BUY if args[2] == "B" else fix.Side_SELL,
                    int(args[3]),
                    float(args[4]),
                )
                return msg
            case "exec":
                msg = OrderFactory.execution_report(
                    order_id=str(args[0]),
                    cl_ord_id=str(args[1]),
                    symbol=str(args[2]),
                    side=fix.Side_BUY if args[3] == "B" else fix.Side_SELL,
                    order_qty=int(args[4]),
                    price=float(args[5]),
                )
                return msg

            case _:
                print("[App]: unknown msg type.")

    def print_help(self):
        print(""" FixCli command line tool. 

        Commands:
            exit|quit, help, raw, new, exec
        """)


class OrderFactory:

    @staticmethod
    def new_limit_order(
        cl_ord_id,
        symbol,
        side,
        qty,
        price,
    ):
        order = fix44.NewOrderSingle()

        order.setField(fix.ClOrdID(cl_ord_id))
        order.setField(fix.HandlInst("1"))
        order.setField(fix.Symbol(symbol))
        order.setField(fix.Side(side))
        order.setField(fix.OrderQty(qty))
        order.setField(fix.OrdType(fix.OrdType_LIMIT))
        order.setField(fix.Price(price))
        order.setField(fix.TransactTime())

        return order

    @staticmethod
    def execution_report(
        order_id: str,
        cl_ord_id: str,
        symbol: str,
        side: str,
        order_qty: float,
        price: float,
        exec_type=fix.ExecType_NEW,
        ord_status=fix.OrdStatus_NEW,
        exec_id: str | None = None,
        leaves_qty: float | None = None,
        cum_qty: float = 0,
        avg_px: float = 0,
    ) -> fix44.ExecutionReport:

        report = fix44.ExecutionReport()

        report.setField(fix.OrderID(order_id))
        report.setField(fix.ExecID(exec_id or str(uuid.uuid4())))

        report.setField(fix.ExecType(exec_type))
        report.setField(fix.OrdStatus(ord_status))

        report.setField(fix.ClOrdID(cl_ord_id))

        report.setField(fix.Symbol(symbol))
        report.setField(fix.Side(side))

        report.setField(fix.OrderQty(order_qty))
        report.setField(fix.Price(price))

        report.setField(fix.CumQty(cum_qty))
        report.setField(
            fix.LeavesQty(order_qty - cum_qty if leaves_qty is None else leaves_qty)
        )
        report.setField(fix.AvgPx(avg_px))

        report.setField(fix.TransactTime())

        return report
