import quickfix44 as fix44
import quickfix as fix


class Cli:
    def __init__(self):
        pass

    def prompt_message(self):
        while True:
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

        match command:
            case "exit" | "quit":
                return None, True
            case "help":
                self.print_help()
                return None, False
            case 'nos':
                return self.msg_builder('nos'), True
            case _:
                print("[App]: unknown command.")
                self.print_help()
                return None, False

    def msg_builder(self, msg_type):
        match msg_type:
            case "nos":
                msg = OrderFactory.new_limit_order('12345', 'VALE3', fix.Side_BUY, 100, 1.0)
                return msg

            case _:
                print("[App]: unknown msg type.")

    def print_help(self):
        print(""" FixCli command line tool. 

        Commands:
            exit|quit, help 
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
