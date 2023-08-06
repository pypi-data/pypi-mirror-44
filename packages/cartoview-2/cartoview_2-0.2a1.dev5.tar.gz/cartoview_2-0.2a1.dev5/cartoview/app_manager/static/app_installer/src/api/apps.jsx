import { ApiRequests } from './utils'
const requests = new ApiRequests()
export function getStoresApps(store) {
	return requests.doExternalGet(`${store.url}app/?server_type__name=${store.server_type}&cartoview_version=${window.appInstallerProps.cartoview_version}`)
}
export function getInstalledApps() {
	const { urls } = window.appInstallerProps
	return requests.doGet(urls.appsURL)
}
function getAppByName(installedApps, name) {
	let app = installedApps.find(app => app.name === name)
	let index = installedApps.findIndex(app => app.name === name)
	return [app, index]
}
export function mergeApps(storeApps, installedApps) {
	for (let index = 0; index < storeApps.length; index++) {
		let app = storeApps[index]
		let installedApp = getAppByName(installedApps, app.name)
		if (installedApp[0]) {
			app.installedApp = installedApp[0]
		} else {
			app.installedApp = undefined

		}
	}
	return storeApps
}