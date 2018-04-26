import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import GridList, { GridListTile, GridListTileBar } from 'material-ui/GridList'
import IconButton from 'material-ui/IconButton'
import InfoIcon from '@material-ui/icons/Info'
import image from './breakfast.jpg'

const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.paper
  },
  gridList: {
    width: 500,
    height: 500
  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)'
  }
})

const tileData = [
  {
    img: image,
    title: 'Image',
    author: 'author'
  }
]

class TitlebarGridList extends React.Component {
  constructor (props) {
    super()
    this.props = props
  }

  render () {
    const { classes } = this.props

    return (
      <div className={classes.root}>
        <GridList cellHeight={180} className={classes.gridList}>
          <GridListTile key='Subheader' cols={2} style={{ height: 'auto' }} />
          {tileData.map(tile => (
            <GridListTile key={tile.img}>
              <img src={tile.img} alt={tile.title} />
              <GridListTileBar
                actionIcon={
                  <IconButton className={classes.icon}>
                    <InfoIcon />
                  </IconButton>
                }
              />
            </GridListTile>
          ))}
        </GridList>
      </div>
    )
  }
}

TitlebarGridList.propTypes = {
  classes: PropTypes.object.isRequired
}

export default withStyles(styles)(TitlebarGridList)
