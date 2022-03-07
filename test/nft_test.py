import pytest
import json
from assembly.lang_9 import ContractRef

NFT = ContractRef('nft', '1.0.0', 9)

class TestNFT():

    @pytest.fixture
    def reset_publish(self, network):
        network.reset(sympl_version=9)
        network.publish([NFT])

    @pytest.fixture
    def key_alias(self, network):
        return network.register_key_alias()

    @pytest.fixture
    def nft(self, network, reset_publish, key_alias):
        return network[key_alias].nft['9-1.0.0']

    def test_nft_life_cycle(self, nft):
        assert len(nft.get_nfts()) == 0

        new_nft = nft.create_nft(name='SymNyan', symbol='~=[,,_,,]:3', owner_address='eth://sendmemoney', max_mint=None, metadata="")

        assert new_nft['name'] == 'SymNyan'
        assert len(nft.get_nfts()) == 1
        nft.creator_of(id=new_nft['id'])['address'] == 'eth://sendmemoney'

    def test_can_mint(self, nft):
        new_nft = nft.create_nft(name='SymNyan v2', symbol='~=[,,,_,,,]:3', owner_address='eth://sendmemoney', max_mint=None, metadata="")

        nft.creator_of(id=new_nft['id'])['address'] == 'eth://sendmemoney'
        retrieved_nft = nft.get_nft(id=new_nft['id'])
        assert retrieved_nft['balances']['eth://sendmemoney'] == '1'

        nft.mint(to='eth://sendmemoney', nft_id=new_nft['id'])
        reretrieved_nft = nft.get_nft(id=new_nft['id'])
        assert reretrieved_nft['balances']['eth://sendmemoney'] == '2'

    def test_cannot_overmint(self, nft):
        new_nft = nft.create_nft(name='SymNyan v2.5', symbol='~=[,,,__,,,]:3', owner_address='eth://sendmemoney', max_mint=1, metadata="")

        nft.creator_of(id=new_nft['id'])['address'] == 'eth://sendmemoney'
        retrieved_nft = nft.get_nft(id=new_nft['id'])
        assert retrieved_nft['balances']['eth://sendmemoney'] == '1'

        with pytest.raises(Exception):
            nft.mint(to='eth://sendmemoney', nft_id=new_nft['id'])

        reretrieved_nft = nft.get_nft(id=new_nft['id'])
        assert reretrieved_nft['balances']['eth://sendmemoney'] == '1'

    def test_can_burn(self, nft):
        new_nft = nft.create_nft(name='SymNyan v3', symbol='~=[,,,,_,,,,]:3', owner_address='eth://sendmemoney', max_mint=None, metadata="")

        nft.creator_of(id=new_nft['id'])['address'] == 'eth://sendmemoney'
        retrieved_nft = nft.get_nft(id=new_nft['id'])
        assert retrieved_nft['balances']['eth://sendmemoney'] == '1'

        nft.burn(to='eth://sendmemoney', nft_id=new_nft['id'])
        reretrieved_nft = nft.get_nft(id=new_nft['id'])
        assert reretrieved_nft['balances']['eth://sendmemoney'] == '0'

    def test_cannot_overburn(self, nft):
        new_nft = nft.create_nft(name='SymNyan v4', symbol='~=[,,,,,_,,,,,]:3', owner_address='eth://sendmemoney', max_mint=None, metadata="")

        nft.creator_of(id=new_nft['id'])['address'] == 'eth://sendmemoney'
        retrieved_nft = nft.get_nft(id=new_nft['id'])
        assert retrieved_nft['balances']['eth://sendmemoney'] == '1'

        nft.burn(to='eth://sendmemoney', nft_id=new_nft['id'])
        reretrieved_nft = nft.get_nft(id=new_nft['id'])
        assert reretrieved_nft['balances']['eth://sendmemoney'] == '0'

        with pytest.raises(Exception):
            nft.burn(to='eth://sendmemoney', nft_id=new_nft['id'])

    def test_metadata_attached_to_NFT(self, nft):
        new_nft = nft.create_nft(name='SymNyan v4'
                                , symbol='~=[,,,,,_,,,,,]:3'
                                , owner_address='eth://sendmemoney'
                                , max_mint=None
                                , metadata='{"hello": "world"}')

        retrieved_nft = nft.get_nft(id=new_nft['id'])
        assert json.loads(retrieved_nft['metadata'])['hello'] == 'world'

    def test_nft_transfer(self, nft):
        bob_address = 'eth://sendmemoney'
        alice_address = 'algo://thisisanalgowallet'
        new_nft = nft.create_nft(name='SymNyan v4'
                                , symbol='~=[,,,,,_,,,,,]:3'
                                , owner_address= alice_address
                                , max_mint=None
                                , metadata='{"hello": "world"}')

        retrieved_nft = nft.get_nft(id=new_nft['id'])
        assert retrieved_nft['balances'][alice_address] == '1'

        nft.transfer(_from=alice_address, to=bob_address, nft_id=new_nft['id'])
        reretrieved_nft = nft.get_nft(id=new_nft['id'])
        assert reretrieved_nft['balances'][alice_address] == '0'
        assert reretrieved_nft['balances'][bob_address] == '1'
