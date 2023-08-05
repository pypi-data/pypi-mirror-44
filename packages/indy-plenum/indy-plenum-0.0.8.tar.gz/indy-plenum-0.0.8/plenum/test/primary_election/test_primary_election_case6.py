import pytest

from plenum.common.messages.node_messages import Nomination, Reelection, Primary
from plenum.test.delayers import delay
from plenum.test.helper import sdk_send_random_and_check
from plenum.test.test_node import checkNodesConnected, \
    checkProtocolInstanceSetup
from stp_core.loop.eventually import eventually


@pytest.fixture(scope='module')
def case_6_setup(txnPoolNodeSet):
    A, B, C, D = txnPoolNodeSet

    # A will get Nomination, Primary, Reelection from after elections get over
    for m in (Nomination, Primary, Reelection):
        delay(m, frm=B, to=A, howlong=120)

    # A will get Primary earlier than Nominates
    delay(Nomination, frm=(C, D), to=A, howlong=10)


# noinspection PyIncorrectDocstring
@pytest.fixture(scope='module')
def elections_done(case_6_setup, looper, txnPoolNodeSet):
    # Make sure elections are done successfully
    A, B, C, D = txnPoolNodeSet
    looper.run(checkNodesConnected(txnPoolNodeSet))

    inst_ids = (0, 1)

    def chk():
        # Check that each Primary is received by A before A has sent any
        # Primary
        primary_recv_times = {
            i: [entry.starttime for entry in A.elector.spylog.getAll(
                A.elector.processPrimary) if entry.params['prim'].instId == i]
            for i in inst_ids
        }
        primary_send_times = {
            i: [entry.starttime for entry in A.elector.spylog.getAll(
                A.elector.sendPrimary) if entry.params['instId'] == 0]
            for i in inst_ids
        }

        for i in inst_ids:
            assert primary_send_times[i][0] > max(primary_recv_times[i])

    looper.run(eventually(chk, retryWait=1, timeout=15))
    checkProtocolInstanceSetup(looper=looper, nodes=txnPoolNodeSet, retryWait=1)

    # Make sure no Nominations or Primary are received by A from B
    for i in inst_ids:
        assert B.replicas[i].name not in A.elector.nominations[i]
        assert B.replicas[i].name not in A.elector.primaryDeclarations[i]


@pytest.mark.skip('Nodes use round robin primary selection')
def test_primary_election_case6(elections_done, txnPoolNodeSet, looper,
                                sdk_pool_handle,
                                sdk_wallet_steward):
    """
    A is disconnected with B so A does not get any Nomination/Primary from
    B (simulated by a large delay). A gets Nominations delayed due to which is
    sends Primary only after it has received Primary from other 2 nodes.
    A should still be able to select a primary and the pool should function.
    """
    sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                              sdk_wallet_steward, 5)
