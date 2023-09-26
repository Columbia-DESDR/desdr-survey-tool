import React, {useEffect, useState} from "react";
import {Content, Dropdown, DropdownLi, DropdownUl, Wrapper} from "./styled";
import {useSelect} from "downshift";
import {axiosInstance} from "../../../../config/http";
import {get} from "lodash";

export default function Analysis() {
  const [deployments, setDeployments] = useState([])
  const [deploymentStats, setDeploymentStats] = useState({})

  const itemToString = (item) => {
    return item.deployment_name + ' (' + item.instance_name + ')'
  }

  const {
    isOpen,
    selectedItem,
    getToggleButtonProps,
    getMenuProps,
    highlightedIndex,
    getItemProps,
  } = useSelect({
    items: deployments,
    itemToString,
  })

  useEffect(() => {
    axiosInstance.get('/deployment').then(response => {
      console.log(response)
      let deployments = get(response, 'data', [])
      setDeployments(deployments)
    }).catch(error => {
      console.log(error)
    })
  }, [])

  useEffect(() => {
    if (selectedItem) {
      axiosInstance.get('/deployment-stats?deployment_name=' + selectedItem.deployment_name).then(response => {
        let deployment_stats = get(response, 'data', [])
        let totalInitiations = 0
        let totalCompletions = 0
        let totalUniqueInitiations = 0
        let totalUniqueCompletions = 0
        let stats = {}
        if (deployment_stats.step_wise_stats.length > 0) {
          for (const i in deployment_stats.step_wise_stats) {
            const dep = deployment_stats.step_wise_stats[i]
            stats[dep.step_name + '_' + i.toString()] = {...dep}
            if (dep.step_name === 'start') {
              totalInitiations += dep.cnt
            }
            if (dep.step_name === '$END_SURVEY$') {
              totalCompletions += dep.cnt
            }
          }
        }
        if (deployment_stats.step_wise_unique_stats.length > 0) {
          for (const i in deployment_stats.step_wise_unique_stats) {
            const dep = deployment_stats.step_wise_unique_stats[i]
            stats[dep.step_name + '_' + i.toString()].uniqueCnt = dep.cnt
            if (dep.step_name === 'start') {
              totalUniqueInitiations += dep.cnt
            }
            if (dep.step_name === '$END_SURVEY$') {
              totalUniqueCompletions += dep.cnt
            }
          }
        }

        setDeploymentStats({
          totalInitiations: totalInitiations,
          totalUniqueInitiations: totalUniqueInitiations,
          totalCompletions: totalCompletions,
          totalUniqueCompletions: totalUniqueCompletions,
          stats: Object.values(stats)
        })

      }).catch(error => {
        console.log(error)
      })
    }
  }, [selectedItem])


  return (
    <Wrapper>
      <div style={{width: 'fit-content', minWidth: '210px'}}>
        <div style={{marginBottom: '5px'}}>Survey: </div>
        <Dropdown
          {...getToggleButtonProps()}
        >
          <span>{selectedItem ? itemToString(selectedItem) : 'Select a survey'}</span>
          <span style={{float: 'right'}}>{isOpen ? <>&#8593;</> : <>&#8595;</>}</span>
        </Dropdown>
        <DropdownUl
          isOpen={isOpen}
          {...getMenuProps()}
        >
          {isOpen &&
            deployments.map((item, index) => (
              <DropdownLi
                isHighlighted={highlightedIndex === index}
                isSelected={selectedItem === item}
                key={`${item.value}${index}`}
                {...getItemProps({item, index})}
              >
                <span>{itemToString(item)}</span>
              </DropdownLi>
            ))}
        </DropdownUl>
      </div>
      {
        selectedItem &&
        <Content>
          <div>Total Initiations: {deploymentStats.totalInitiations}</div>
          <div>Total Unique Initiations: {deploymentStats.totalUniqueInitiations}</div>
          <div>Total Completions: {deploymentStats.totalCompletions}</div>
          <div>Total Unique Completions: {deploymentStats.totalUniqueCompletions}</div>
          <br/>
          {
            deploymentStats.stats && deploymentStats.stats.length > 0 &&
            <table>
              <thead>
              <tr>
                <th>Step name</th>
                <th>Question</th>
                <th>Response count</th>
                <th>Unique response count</th>
              </tr>
              </thead>
              <tbody>
              {
                deploymentStats.stats.map(stat => <tr>
                  <td>{stat.step_name}</td>
                  <td>{stat.question}</td>
                  <td>{stat.cnt}</td>
                  <td>{stat.uniqueCnt}</td>
                </tr>)
              }
              </tbody>
            </table>
          }
        </Content>
      }

    </Wrapper>
  )
}