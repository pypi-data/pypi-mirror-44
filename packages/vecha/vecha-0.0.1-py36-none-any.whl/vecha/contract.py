from request import Request, post
from vemodel import FunctionCoder, EventDecoder
from typing import Dict, List, Iterator


from chain import Chain
from function import Function


class Contract(object):

    def __init__(self, endpoint: str, address: str, abi_list: List):
        super(Contract, self).__init__()

        self.address = address
        self.request = Request(endpoint)
        self.chain = Chain(endpoint)

        event_abi_list = filter(lambda x: x.get('type', '') == 'event', abi_list)
        self.event_decoder = EventDecoder(*event_abi_list)

        fn_abi_list = filter(lambda x: x.get('type', '') == 'function', abi_list)
        self.fn_coder = FunctionCoder(*fn_abi_list)

    def __getattr__(self, fn_name):
        fn = Function(self.chain, self.address, self.request, self.fn_coder, self.event_decoder, fn_name)

        if self.fn_coder.is_call(fn_name):
            return fn.call
        else:
            return fn

    def get_events(self, start_block_num: int = 0, to_block_num: int = None, event_id: str = None) -> Iterator:
        to_block_num = to_block_num if to_block_num else self.chain.best_blcok_num()
        query = {
            'range': {
                'unit': 'block',
                'from': start_block_num,
                'to': to_block_num
            },
            'criteriaSet': [
                {
                    'address': self.address,
                    'topic0': event_id
                }
            ]
        }
        event_list = self.request.logs.event.make_request(post, data=query)
        return filter(lambda x: x, map(self.event_decoder.decode_event, event_list))


if __name__ == '__main__':
    import json

    def get_abi_from_file(file_path: str):
        with open('contract.json', 'r') as contract_file:
            contract_json = contract_file.read()
        contract = json.loads(contract_json)
        return contract['abi']

    c = Contract(
        'https://sync-testnet.vechain.org',
        '0x72Ca1aafE8E8f84ABbFba3705c35F084eCd21989',
        get_abi_from_file('contract.json')
    )
    # r = c.getQuiz(1)
    # print(r)

    r = c.creat.call(
        47548766,
        1553677200,
        '2019 LPL 春季赛-常规赛',
        'FPX',
        'VG',
        # value=0,
        # pk='88d2d80b12b92feaa0da6d62309463d20408157723f2d7e799b6a74ead9a673b'
    )
    print(r)
