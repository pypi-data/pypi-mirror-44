
import { connect } from 'react-redux';
import { deletePayment, fetchProjects, openPaymentDialog } from '../actions';
import { ExpandedPayment, State, ThunkDispatcher } from '../types';
import PaymentList, {OwnProps, StateProps, DispatchProps} from '../components/PaymentList';

function mapStateToProps(state: State, props: OwnProps) {
    const {payments, users} = state;

    let paymentRows = [];
    for (const payment of Object.values(payments).filter(p => p.projectId == props.id)) {

        let exPayment: ExpandedPayment = {
            ...payment,
            createdUserName: (payment.createdUserId in users) ? users[payment.createdUserId].name : '',
            paidUserName: (payment.paidUserId in users) ? users[payment.paidUserId].name : ''
        }
        paymentRows.push(exPayment)
    }
    return {
        rows: paymentRows,
    }
}

const mapDispatchToProps = (dispatch: ThunkDispatcher) => {
    return {
        onDelete: (payment: ExpandedPayment) => {
            const projectId = payment.projectId;
            if (confirm('Do you really want to delete this payment?'))
                dispatch(deletePayment(payment.id)).then(() => {
                    dispatch(fetchProjects(projectId))
                })
        },
        onAddPayment: (projectId: number) => {
            dispatch(openPaymentDialog(projectId))
        },
    }
}

export default connect<StateProps, DispatchProps, OwnProps>(mapStateToProps, mapDispatchToProps)(PaymentList);
