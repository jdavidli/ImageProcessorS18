import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import {AreaChart, Area, XAxis, YAxis} from 'recharts'
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table'

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
      open: false,
      open2: false,
      tile: null
    }
  }

  render () {
    const { classes } = this.props
    const origTileData = this.props.oTile

    const procTileData = this.props.pTile

    return (

      <div className={classes.root}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Original Image</TableCell>
              <TableCell>Upload Time</TableCell>
              <TableCell>Image Size</TableCell>
              <TableCell>Original Histogram </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {origTileData.map(n => {
              return (
                <TableRow>
                  <TableCell><img src={n.img} style={{width: 500}} /></TableCell>
                  <TableCell>{n.uptime}</TableCell>
                  <TableCell>{n.upsize}</TableCell>
                  <TableCell>{<AreaChart width={500} height={400} data={n.oHist}
                    margin={{top: 10, right: 10, left: 0, bottom: 0}}>
                    <XAxis ticks={[0, 255]} />
                    <YAxis />
                    <Area type='monotone' dataKey='R' stackId='1' stroke='#8884d8' fill='#8884d8' />
                  </AreaChart>}</TableCell>
                </TableRow>
              )
            })}
          </TableBody>
        </Table>

        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Processed Image</TableCell>
              <TableCell>Processing Time</TableCell>
              <TableCell>Image Size</TableCell>
              <TableCell>Processed Histogram </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {procTileData.map(m => {
              return (
                <TableRow>
                  <TableCell><img src={m.img} style={{width: 500}} /></TableCell>
                  <TableCell>{m.proctime}</TableCell>
                  <TableCell>{m.upsize}</TableCell>
                  <TableCell>{<AreaChart width={500} height={400} data={m.pHist}
                    margin={{top: 10, right: 10, left: 0, bottom: 0}}>
                    <XAxis ticks={[0, 255]} />
                    <YAxis />
                    <Area type='monotone' dataKey='R' stackId='1' stroke='#8884d8' fill='#8884d8' />
                  </AreaChart>}</TableCell>
                </TableRow>
              )
            })}
          </TableBody>
        </Table>
      </div>
    )
  }
}

TitlebarGridList.propTypes = {
  classes: PropTypes.object.isRequired
}

export default withStyles(styles)(TitlebarGridList)
