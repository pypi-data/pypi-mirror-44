import * as filterActions from '../actions/filter'

import { Icon, Pagination } from 'semantic-ui-react'

import PropTypes from 'prop-types'
import React from 'react'
import { connect } from 'react-redux'

class AppsPagination extends React.Component {
	handlePaginationChange = (e, { activePage }) => {
		this.props.setActivePage(activePage)
	}
	getTotalPages = () => {
		const { apps, appFilters } = this.props
		return Math.ceil(apps.storeCount / appFilters.itemsPerPage)
	}
	render() {
		const { appFilters } = this.props
		return (
			<Pagination
				activePage={appFilters.activePage}
				onPageChange={this.handlePaginationChange}
				totalPages={this.getTotalPages()}
				ellipsisItem={{ content: <Icon name='ellipsis horizontal' />, icon: true }}
				firstItem={{ content: <Icon name='angle double left' />, icon: true }}
				lastItem={{ content: <Icon name='angle double right' />, icon: true }}
				prevItem={{ content: <Icon name='angle left' />, icon: true }}
				nextItem={{ content: <Icon name='angle right' />, icon: true }}
			/>
		)
	}
}
AppsPagination.propTypes = {
	setActivePage: PropTypes.func.isRequired,
	apps: PropTypes.object.isRequired,
	appFilters: PropTypes.object.isRequired,
}
const mapStateToProps = (state) => {
	return {
		apps: state.apps,
		appFilters: state.appFilters,
	}
}
const mapDispatchToProps = (dispatch) => {
	return {
		setActivePage: (pageNumber) => dispatch(filterActions.setActivePage(pageNumber)),
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(AppsPagination)