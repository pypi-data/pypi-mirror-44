import { Button, Card, Placeholder } from 'semantic-ui-react'

import PropTypes from 'prop-types'
import React from 'react'

const CardsLoading = (props) => {
	return (
		< Card.Group centered>
			{Array(props.cardsCount).fill().map((_, i) => {
				return <Card centered key={i} >
					<Placeholder>
						<Placeholder.Image square />
					</Placeholder>
					<Card.Content>
						<Placeholder>
							<Placeholder.Header>
								<Placeholder.Line length='very short' />
								<Placeholder.Line length='medium' />
							</Placeholder.Header>
							<Placeholder.Paragraph>
								<Placeholder.Line length='short' />
							</Placeholder.Paragraph>
						</Placeholder>
					</Card.Content>

					<Card.Content extra>
						<div className='ui three buttons'>
							<Button basic disabled color='green'>
								{"Install"}
							</Button>
							<Button basic disabled color='red'>
								{"Uninstall"}
							</Button>
							<Button basic disabled color='red'>
								{"Suspend"}
							</Button>
						</div>
					</Card.Content>
				</Card>
			})}
		</Card.Group>
	)
}
CardsLoading.propTypes = {
	cardsCount: PropTypes.number.isRequired
}
CardsLoading.defaultProps = {
	cardsCount: 9
}
export default CardsLoading