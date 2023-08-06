import {
	Container,
	Dropdown,
	Image,
	Menu,
} from 'semantic-ui-react'

import React from 'react'
import logoIMG from '../img/logo.png'

export const NavBar = (props) => {
	return (
		<Menu fixed='top' inverted>
			<Container>
				<Menu.Item as='a' header>
					<Image size='small' src={logoIMG} style={{ marginRight: '1.5em' }} />
				</Menu.Item>
				<Menu.Item as='a' href={"/"}>{"Home"}</Menu.Item>

				<Dropdown item simple text='Dropdown'>
					<Dropdown.Menu>
						<Dropdown.Item>List Item</Dropdown.Item>
						<Dropdown.Item>List Item</Dropdown.Item>
						<Dropdown.Divider />
						<Dropdown.Header>{"Header Item"}</Dropdown.Header>
						<Dropdown.Item>
							<i className='dropdown icon' />
							<span className='text'>Submenu</span>
							<Dropdown.Menu>
								<Dropdown.Item>List Item</Dropdown.Item>
								<Dropdown.Item>List Item</Dropdown.Item>
							</Dropdown.Menu>
						</Dropdown.Item>
						<Dropdown.Item>List Item</Dropdown.Item>
					</Dropdown.Menu>
				</Dropdown>
			</Container>
		</Menu>
	)
}
export default NavBar