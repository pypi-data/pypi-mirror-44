import { ApiRequests } from './utils'
const requests = new ApiRequests()
export function getStores() {
	const { urls } = window.appInstallerProps
	return requests.doGet(urls.storesURL)
}