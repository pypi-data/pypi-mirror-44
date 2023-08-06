import * as errorActions from '../actions/errors'

import { Icon, Message } from 'semantic-ui-react'

import PropTypes from 'prop-types'
import React from 'react'
import { connect } from 'react-redux'

class ErrorList extends React.Component {
	render() {
		const { appErrors, deleteError } = this.props
		return (
			<div>
				{appErrors.errors.map((err, index) => {
					return <Message
						onDismiss={() => deleteError(err)}
						key={index}
						header='Error!'
						icon={<Icon name="info circle" />}
						content={err}
					/>
				})}
			</div>
		)
	}
}
ErrorList.propTypes = {
	appErrors: PropTypes.object.isRequired,
	deleteError: PropTypes.func.isRequired,
}
const mapStateToProps = (state) => {
	return {
		appErrors: state.appErrors,
	}
}
const mapDispatchToProps = (dispatch) => {
	return {
		deleteError: (error) => dispatch(errorActions.deleteError(error)),
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(ErrorList)