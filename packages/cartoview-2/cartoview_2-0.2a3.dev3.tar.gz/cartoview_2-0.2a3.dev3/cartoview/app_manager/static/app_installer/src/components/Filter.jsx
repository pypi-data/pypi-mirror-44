import * as filterActions from '../actions/filter'

import { Form, Segment, Input, Icon } from 'semantic-ui-react'

import PropTypes from 'prop-types'
import React from 'react'
import { connect } from 'react-redux'

const sortTypeOptions = [
	{ key: 't', text: 'Ascending', value: 'asc' },
	{ key: 'f', text: 'Descending', value: 'desc' },
]
const sortByOptions = [
	{ key: 't', text: 'Title', value: 'title' },
	{ key: 'c', text: 'Compatibility', value: 'compatible' },
	{ key: 'd', text: 'Downloads', value: 'downloads' },
]
class Filters extends React.Component {
	handleChange = (e, { value }) => {
		this.props.setSortBy(value)
	}
	sortTypeChanged = (e, { value }) => {
		this.props.setSortType(value)
	}
	handleTextChange = (e, { value }) => {
		const { setSearchText } = this.props
		setSearchText(value)
	}
	render() {
		const { appFilters } = this.props
		return (<Segment >
			<Form>
				<Form.Field>
					<Input
						icon={<Icon name="search"/>}
						placeholder='Search...'
						value={appFilters.searchText}
						onChange={this.handleTextChange}
					/>
				</Form.Field>
				<Form.Group widths="equal" inline>
					<Form.Select onChange={this.handleChange} label='Sort By' value={appFilters.sortBy} options={sortByOptions} placeholder='Sort Attribute' />
					<Form.Select onChange={this.sortTypeChanged} label='Sort Type' value={appFilters.sortType} options={sortTypeOptions} placeholder='Sort Type' />
				</Form.Group>
			</Form>

		</Segment>)
	}
}
Filters.propTypes = {
	setSortBy: PropTypes.func.isRequired,
	setSearchText: PropTypes.func.isRequired,
	setSortType: PropTypes.func.isRequired,
	apps: PropTypes.object.isRequired,
	appStores: PropTypes.object.isRequired,
	appFilters: PropTypes.object.isRequired,
}
const mapStateToProps = (state) => {
	return {
		apps: state.apps,
		appStores: state.appStores,
		appFilters: state.appFilters
	}
}
const mapDispatchToProps = (dispatch) => {
	return {
		setSortBy: (attributeName) => dispatch(filterActions.setSortBy(attributeName)),
		setSearchText: (text) => dispatch(filterActions.setSearchText(text)),
		setSortType: (text) => dispatch(filterActions.setSortType(text)),
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(Filters)