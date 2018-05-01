import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import GridList, { GridListTile, GridListTileBar } from 'material-ui/GridList'
import IconButton from 'material-ui/IconButton'
import InfoIcon from '@material-ui/icons/Info'
import Dialog, { DialogTitle, DialogContent, DialogContentText} from 'material-ui/Dialog'
import {AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip} from 'recharts'

const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    backgroundColor: theme.palette.background.paper
  },
  gridList: {
    width: 500
  },
  icon: {
    color: 'rgba(255, 255, 255, 0.54)'
  }
})

class TitlebarGridList extends React.Component {
  constructor (props) {
    super()
    this.props = props
    this.state = {
      open: false
    }
  }

  handleClickOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  render () {
    const { classes } = this.props
    const tileData = [
      {
        img: this.props.oImgParent,
        uptime: this.props.uTime,
        proctime: this.props.pTime,
        upsize: this.props.uSize
      },
      {
        img: this.props.pImgParent,
        uptime: this.props.uTime,
        proctime: this.props.pTime,
        upsize: this.props.uSize
      }
    ]

    // graphing
    const preOData = this.props.oHist[0]
    const lgProps = [{ dataKey: 'R', values: preOData}]
    console.log(lgProps)
    var oData = []
    var oJSON = {}
    for (var i in preOData) {
      oData.push({"R": preOData[i]})
    }
    console.log(oData)

    return (
      <div className={classes.root}>
      <GridList cellHeight={200} className={classes.gridList}>
        <GridListTile key='Subheader' cols={2} style={{ height: 'auto' }} />
        {tileData.map((tile, i) => (
          <GridListTile key={tile.img + i}>
            <img src={tile.img} />
            <GridListTileBar
              actionIcon={
                <IconButton className={classes.icon} onClick={this.handleClickOpen}>
                <Dialog
        open={this.state.open}
        onClose={this.handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{"Image Information"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
          <AreaChart width={550} height={400} data={oData}
                margin={{top: 10, right: 10, left: 0, bottom: 0}}>
            <XAxis ticks={[0,255]} />
            <YAxis />
            <Area type='monotone' dataKey='R' stackId="1" stroke='#8884d8' fill='#8884d8' />
          </AreaChart>
            Uploaded time: {tile.uptime}
            <br/>
            Processing time: {tile.proctime}
            <br/>
            Image size: {tile.upsize}
          </DialogContentText>
        </DialogContent>
      </Dialog>
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
