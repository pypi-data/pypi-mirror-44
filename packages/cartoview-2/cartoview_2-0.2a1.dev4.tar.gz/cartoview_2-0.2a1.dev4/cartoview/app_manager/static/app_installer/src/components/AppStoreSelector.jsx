import { Dimmer, Dropdown, Loader, } from 'semantic-ui-react'
import { appStoresLoading, selectAppStore, setAppStores } from '../actions/appStores'

import PropTypes from 'prop-types'
import React from 'react'
import { connect } from 'react-redux'
import { getStores } from '../api/stores'

class AppStoreSelector extends React.Component {
	componentDidMount() {
		const { setStores, setStoresLoading } = this.props
		getStores().then(data => {
			setStores(data.results)
			this.getDefaultStore()
			setStoresLoading(false)
		})
	}
	onChange = (event, { value }) => {
		const { selectStore } = this.props
		selectStore(value)
	}
	getStoresOptions() {
		const { appStores } = this.props
		let storesOptions = appStores.stores.map(store => {
			return {
				text: `${store.name} (${store.server_type})`,
				value: store.id,
			}
		})
		return storesOptions
	}
	getDefaultStore = () => {
		const { appStores, selectStore } = this.props
		let defaultStoreID = undefined
		for (let index = 0; index < appStores.stores.length; index++) {
			const store = appStores.stores[index]
			if (store.is_default) {
				defaultStoreID = store.id
			}

		}
		selectStore(defaultStoreID)
		return defaultStoreID
	}
	render() {
		const { appStores } = this.props
		return (
			<div>
				{
					appStores.loading ? <Dimmer active inverted>
						<Loader inverted content='Loading' />
					</Dimmer> : < Dropdown onChange={this.onChange}
						placeholder='Select an App Store'
						value={appStores.selectedStoreID}
						fluid
						selection
						options={this.getStoresOptions()} />
				}
			</div>

		)
	}
}
AppStoreSelector.propTypes = {
	setStores: PropTypes.func.isRequired,
	setStoresLoading: PropTypes.func.isRequired,
	selectStore: PropTypes.func.isRequired,
	appStores: PropTypes.object.isRequired,
}
const mapStateToProps = (state) => {
	return {
		appStores: state.appStores,
	}
}
const mapDispatchToProps = (dispatch) => {
	return {
		setStores: (stores) => dispatch(setAppStores(stores)),
		setStoresLoading: (loading) => dispatch(appStoresLoading(loading)),
		selectStore: (selectedStoreID) => dispatch(selectAppStore(selectedStoreID)),
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(AppStoreSelector)