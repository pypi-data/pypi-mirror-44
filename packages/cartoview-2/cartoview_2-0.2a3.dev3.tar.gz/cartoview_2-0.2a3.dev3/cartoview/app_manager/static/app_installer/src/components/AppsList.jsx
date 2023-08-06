import * as _ from 'lodash';
import * as appsActions from '../actions/apps'
import * as errorActions from '../actions/errors'
import * as storeActions from '../actions/storeApps'

import { ApiRequests, getCRSFToken } from '../api/utils'
import { Button, Card, Grid, Icon, Image, Label, Popup } from 'semantic-ui-react'
import { getInstalledApps, getStoresApps } from '../api/apps'

import AppFilter from './Filter'
import AppsPagination from './Pagination'
import CardsLoading from './CardsLoading'
import PropTypes from 'prop-types'
import React from 'react'
import { connect } from 'react-redux'
import { versionCompare } from '../api/compare'

const requests = new ApiRequests()
const colorsMapping = {
	"Alpha": "red",
	"Beta": "yellow",
	"Stable": "green"
}
class AppsList extends React.Component {
	componentDidUpdate(prevProps) {
		const { appStores } = prevProps
		if (this.props.appStores.selectedStoreID && appStores.selectedStoreID != this.props.appStores.selectedStoreID) {
			const { setStoreAppsList, setStoreCount, setStoreLoading } = this.props
			let store = this.props.appStores.stores.find(store => store.id === this.props.appStores.selectedStoreID)
			getStoresApps(store).then(data => {
				let storeApps = data.objects.map(storeApp => {
					storeApp.compatible = false
					storeApp.installing = false
					storeApp.uninstalling = false
					const cartoview_versions = storeApp.latest_version.cartoview_version
					for (let index = 0; index < cartoview_versions.length; index++) {
						const cartoview_version = cartoview_versions[index]
						if (versionCompare(cartoview_version.version, window.appInstallerProps.cartoview_version, { 'lexicographical': true }) == 0) {
							storeApp.compatible = true
							break
						}
					}
					return storeApp
				})
				setStoreAppsList(storeApps)
				setStoreCount(data.meta.total_count)
				setStoreLoading(false)
			})
			const { setInstalled, setInstalledLoading, setIntalledCount } = this.props
			getInstalledApps().then(data => {
				setInstalled(data.results)
				setIntalledCount(data.count)
				setInstalledLoading(false)
			})
		}

	}
	sortApps = () => {
		const { apps, appFilters } = this.props

		return _.orderBy(apps.storeApps, [appFilters.sortBy], [appFilters.sortType])
	}
	getTotalPages = () => {
		const { apps, appFilters } = this.props
		return Math.ceil(apps.storeCount / appFilters.itemsPerPage)
	}
	searchApps = (apps) => {
		const { appFilters } = this.props
		if (appFilters.searchText != "") {
			return _.filter(apps, app => {
				let { title, description } = app
				let searchText = appFilters.searchText.toLowerCase()
				title = title.toLowerCase()
				description = description.toLowerCase()
				return title.includes(searchText) || description.includes(searchText)
			})
		}
		return apps

	}
	getApps = () => {
		const { appFilters } = this.props
		let apps = this.sortApps()
		apps = this.searchApps(apps)
		if (appFilters.searchText === "") {
			apps = this.paginate(apps)
		}
		return apps
	}
	paginate = (apps) => {
		const { appFilters } = this.props
		const startIndex = (appFilters.activePage - 1) * appFilters.itemsPerPage
		const endIndex = appFilters.activePage * appFilters.itemsPerPage
		return apps.slice(startIndex, endIndex)
	}
	getInstalledByName = (name) => {
		const { apps } = this.props
		return apps.installed.find(app => app.name == name)
	}
	installApp = (app) => () => {
		const { appStores, setInProgress, updateStoreApp, addInstalledApps, addError } = this.props
		app.installing = true
		setInProgress(true)
		updateStoreApp(app)
		const data = JSON.stringify({
			'app_name': app.name,
			"store_id": appStores.selectedStoreID,
			"app_version": app.latest_version.version
		})
		requests.doPost(window.appInstallerProps.urls.install, data,
			{
				"Content-Type": "application/json",
				"X-CSRFToken": getCRSFToken(),
			}).then(data => {
				if (!Object.keys(data).includes("details")) {
					addInstalledApps([data])
					updateStoreApp({ ...app, compatible: true, installing: false })
					setInProgress(false)
				} else {
					addError([data.details])
				}
			}).catch((error) => {
				app.installing = false
				setInProgress(false)
				updateStoreApp(app)
				addError([error.message])
			})
	}
	uninstallApp = (app) => () => {
		const { deleteInstalledApps, setInProgress, updateStoreApp, addError } = this.props
		let installedApp = this.getInstalledByName(app.name)
		app.uninstalling = true
		setInProgress(true)
		updateStoreApp(app)
		requests.doDelete(window.appInstallerProps.urls.appsURL + `${installedApp.id}/uninstall/`,
			{
				"Content-Type": "application/json",
				"X-CSRFToken": getCRSFToken(),
			}).then(data => {
				if (!Object.keys(data).includes("details")) {
					deleteInstalledApps([data.id])
					updateStoreApp({ ...app, uninstalling: false })
					setInProgress(false)
				} else {
					addError([data.details])
				}
			}).catch((error) => {
				app.uninstalling = false
				setInProgress(false)
				updateStoreApp(app)
				addError([error.message])
			})
	}
	render() {
		const { apps, appStores, appFilters } = this.props
		const totalPages = this.getTotalPages()
		return (
			<div>
				{apps.storeAppsLoading || apps.installedAppsLoading || appStores.loading ?
					<CardsLoading />
					:
					<Grid centered>
						<Grid.Row centered>
							<Grid.Column width={15} textAlign='center'>
								<AppFilter />
							</Grid.Column>
						</Grid.Row>
						<Grid.Row>
							<Grid.Column>
								<Card.Group centered>
									{this.getApps().map(app => {
										let installedApp = this.getInstalledByName(app.name)
										return <Card centered key={app.id}>
											<Image
												wrapped
												fluid
												className="card-img "
												label={{ as: 'a', color: colorsMapping[app.status], content: app.status, ribbon: true }}
												src={app.latest_version.logo} />

											<Card.Content>
												<Card.Header>
													{app.title}
												</Card.Header>
												<Card.Meta>
													<span className='date'>{app.author}</span>
													<Popup size="small" header={"Description"} trigger={<Icon circular name='info' />} content={app.description} />
												</Card.Meta>
											</Card.Content>
											<Card.Content extra>
												<div className='ui three buttons'>
													{installedApp &&
														versionCompare(app.latest_version.version, installedApp.version, { 'lexicographical': true }) > 0 &&
														<Button onClick={this.installApp(app)} loading={app.installing} disabled={!app.compatible || apps.inProgress} basic color={app.compatible ? 'blue' : 'black'}>
															{app.compatible == true ? "Upgrade" : "Incompatible"}
														</Button>}
													{!installedApp && <Button loading={app.installing} onClick={this.installApp(app)} disabled={!app.compatible || apps.inProgress} basic color={app.compatible == true ? 'green' : 'black'}>
														{app.compatible == true ? "Install" : "Incompatible"}
													</Button>}
													{installedApp && <Button loading={app.uninstalling} onClick={this.uninstallApp(app)} disabled={apps.inProgress} basic color='red'>
														{"Uninstall"}
													</Button>}
													{installedApp && <Button disabled={apps.inProgress} basic color='yellow'>
														{"Suspend"}
													</Button>}

												</div>
											</Card.Content>
											<Card.Content extra>
												<Grid centered>
													<Grid.Row centered columns={installedApp ? 2 : 1}>
														{installedApp && <Grid.Column textAlign="center">
															<Label size="tiny">
																<Icon name='hdd' />
																{`Installed:v${installedApp.version}`}
															</Label>
														</Grid.Column>}
														<Grid.Column textAlign="center">
															<Label color='blue' size="tiny">
																<Icon name='download' />
																{`Latest:v${app.latest_version.version}`}
															</Label>
														</Grid.Column>
													</Grid.Row>
												</Grid>
											</Card.Content>
										</Card>
									})}
								</Card.Group>
							</Grid.Column>
						</Grid.Row>
						{!apps.storeAppsLoading && !apps.installedAppsLoading && !appStores.loading && appFilters.searchText === "" && totalPages > 0 && <Grid.Row centered>
							<Grid.Column textAlign="center">
								<AppsPagination />
							</Grid.Column>
						</Grid.Row>}
					</Grid>
				}
			</div>
		)
	}
}
AppsList.propTypes = {
	setInstalled: PropTypes.func.isRequired,
	setInstalledLoading: PropTypes.func.isRequired,
	setIntalledCount: PropTypes.func.isRequired,
	setStoreAppsList: PropTypes.func.isRequired,
	setStoreLoading: PropTypes.func.isRequired,
	setStoreCount: PropTypes.func.isRequired,
	setInProgress: PropTypes.func.isRequired,
	apps: PropTypes.object.isRequired,
	appFilters: PropTypes.object.isRequired,
	appStores: PropTypes.object.isRequired,
	updateStoreApp: PropTypes.func.isRequired,
	addInstalledApps: PropTypes.func.isRequired,
	deleteInstalledApps: PropTypes.func.isRequired,
	addError: PropTypes.func.isRequired,
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
		setInstalled: (apps) => dispatch(appsActions.setInstalledApps(apps)),
		setInstalledLoading: (loading) => dispatch(appsActions.installedAppsLoading(loading)),
		setIntalledCount: (count) => dispatch(appsActions.installedAppsTotalCount(count)),
		setStoreAppsList: (apps) => dispatch(storeActions.setStoreApps(apps)),
		setStoreLoading: (loading) => dispatch(storeActions.storeAppsLoading(loading)),
		setStoreCount: (count) => dispatch(storeActions.storeAppsTotalCount(count)),
		setInProgress: (loading) => dispatch(appsActions.actionInProgress(loading)),
		updateStoreApp: (app) => dispatch(storeActions.updateStoreApp(app)),
		addInstalledApps: (apps) => dispatch(appsActions.addApps(apps)),
		addError: (error) => dispatch(errorActions.addError(error)),
		deleteInstalledApps: (apps) => dispatch(appsActions.deleteInstalledApps(apps)),
	}
}

export default connect(mapStateToProps, mapDispatchToProps)(AppsList)