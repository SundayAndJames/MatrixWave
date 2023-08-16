<script>
  import { onMount } from "svelte";
  import {
    selectedRectNumber,
    showPath,
    selectedStep,
    selectedNodeIds,
    ifSelected,
    currentSelectedNodeIds,
    websiteArray,
    opacityIds,
    clickFlow1,
    clickFlow2,
    filterFlow1,
    filterFlow2,
    websiteIndexArray,
    pathPositionOfLink,
    pathPositionOfNode,
  } from "../store";
  let nextStepSavdeNode = []; //下一步可以被选中的节点
  let afterSelectedSavedInsideLink = []; //选择完毕后存在路径的InsideLink被保留
  let afterSelectedSavedOutsideLink = []; //选择完毕后存在路径的OutSideLink被保留
  /////////////////////////////////////////////////////////////////////////////////
  //下一步
  function updateSelectedStep() {
    console.log("更新前currentSelectedNodeIds:", $currentSelectedNodeIds);
    //更新selectedNodeIds
    selectedNodeIds.update((data) => {
      let added = [...$currentSelectedNodeIds];
      return [...data, added];
    });
    console.log("更新后selectedNodeIds", $selectedNodeIds);
    filterPath(); //过滤路径
    handleOpacity(); //虚化
    drawPath(); //画出路径
    $selectedStep += 1;
    $currentSelectedNodeIds = [];
    console.log("更新后currentSelectedNodeIds:", $currentSelectedNodeIds);
  }
  //重置
  function resetSelectedStep() {
    $selectedStep = 0;
    $selectedRectNumber = 0;
    //恢复矩形边框
    for (let i = 0; i < $selectedNodeIds.length; i++) {
      for (let j = 0; j < $selectedNodeIds[i].length; j++) {
        let rectNode = document.getElementById($selectedNodeIds[i][j][0]);
        rectNode.style.stroke = "black";
        rectNode.style.strokeWidth = "1px";
      }
    }
    $selectedNodeIds = [];
    ifSelected.update((values) => {
      return values.map((row) => row.map(() => false));
    });
    console.log($selectedNodeIds);
    //恢复opacity为100%
    for (let i = 0; i < $opacityIds.length; i++) {
      let svgElement = document.getElementById($opacityIds[i]);
      svgElement.setAttribute("opacity", "1");
    }
    opacityIds.set([]);
    //更新store
    currentSelectedNodeIds.set([]); //保存当前step选中的节点id
    websiteArray.set([]); //保存网站名称
    filterFlow1.update((data) => [...$clickFlow1]);
    filterFlow2.update((data) => [...$clickFlow2]);
  }
  /////////////////////////////////////////////////////////////////////////////////
  //处理虚化
  function handleOpacity() {
    //1.处理未被选中的虚化：包括相应的node、link、website虚化
    for (let i = 0; i < $websiteArray[$selectedStep].length; i++) {
      //是否被选中
      let ifInSelected = false;
      for (let j = 0; j < $currentSelectedNodeIds.length; j++) {
        if (`nodeRect${i}${$selectedStep}` == $currentSelectedNodeIds[j][0]) {
          ifInSelected = true;
          break;
        }
      }
      //对未被选中的部分进行虚化
      if (!ifInSelected) {
        let nodeRect = document.getElementById(`nodeRect${i}${$selectedStep}`);
        // console.log(nodeRect);
        nodeRect.setAttribute("opacity", "0.2"); // 设置透明度为20%
        let websiteText = document.getElementById(`text${$selectedStep}${i}`);
        websiteText.setAttribute("opacity", "0.2"); // 设置透明度为20%
        opacityIds.update((value) => {
          return [
            ...value,
            `nodeRect${i}${$selectedStep}`,
            `text${$selectedStep}${i}`,
          ];
        });
        //未被选中的下一步link虚化
        for (
          let j = 0;
          $selectedStep < $websiteArray.length - 1 &&
          j < $websiteArray[$selectedStep + 1].length;
          j++
        ) {
          try {
            let linkRectOutside = document.getElementById(
              `linkRectOutside${$selectedStep}${i}${j}`
            );
            let linkRectInside = document.getElementById(
              `linkRectInside${$selectedStep}${i}${j}`
            );
            linkRectOutside.setAttribute("opacity", "0.2"); // 设置透明度为20%
            linkRectInside.setAttribute("opacity", "0.2"); // 设置透明度为20%
            opacityIds.update((values) => {
              return [
                ...values,
                `linkRectOutside${$selectedStep}${i}${j}`,
                `linkRectInside${$selectedStep}${i}${j}`,
              ];
            });
          } catch (error) {
            continue;
          }
        }
        //未被选中的上一步link虚化
        for (
          let j = 0;
          $selectedStep - 1 >= 0 && j < $websiteArray[$selectedStep - 1].length;
          j++
        ) {
          try {
            let linkRectOutside = document.getElementById(
              `linkRectOutside${$selectedStep - 1}${j}${i}`
            );
            let linkRectInside = document.getElementById(
              `linkRectInside${$selectedStep - 1}${j}${i}`
            );
            linkRectOutside.setAttribute("opacity", "0.2"); // 设置透明度为20%
            linkRectInside.setAttribute("opacity", "0.2"); // 设置透明度为20%
            opacityIds.update((values) => {
              return [
                ...values,
                `linkRectOutside${$selectedStep - 1}${j}${i}`,
                `linkRectInside${$selectedStep - 1}${j}${i}`,
              ];
            });
          } catch (error) {
            continue;
          }
        }
      }
    }
    //选中后，保留下一步能够被选中的node
    for (
      let i = 0;
      $selectedStep + 1 < $websiteArray.length &&
      i < $websiteArray[$selectedStep + 1].length;
      i++
    ) {
      if (!nextStepSavdeNode.includes($websiteArray[$selectedStep + 1][i])) {
        let nodeRect = document.getElementById(
          `nodeRect${i}${$selectedStep + 1}`
        );
        nodeRect.setAttribute("opacity", "0.2");
        let websiteText = document.getElementById(
          `text${$selectedStep + 1}${i}`
        );
        websiteText.setAttribute("opacity", "0.2");
        opacityIds.update((value) => {
          return [
            ...value,
            `nodeRect${i}${$selectedStep + 1}`,
            `text${$selectedStep + 1}${i}`,
          ];
        });
        for (let j = 0; j < $websiteArray[$selectedStep].length; j++) {
          try {
            let linkRectOutside = document.getElementById(
              `linkRectOutside${$selectedStep}${j}${i}`
            );
            let linkRectInside = document.getElementById(
              `linkRectInside${$selectedStep}${j}${i}`
            );
            linkRectOutside.setAttribute("opacity", "0.2"); // 设置透明度为20%
            linkRectInside.setAttribute("opacity", "0.2"); // 设置透明度为20%
            opacityIds.update((values) => {
              return [
                ...values,
                `linkRectOutside${$selectedStep}${j}${i}`,
                `linkRectInside${$selectedStep}${j}${i}`,
              ];
            });
          } catch (error) {
            continue;
          }
        }
      }
    }
    //将残余的不存在路径的link虚化
    for (let i = 0; i < $currentSelectedNodeIds.length; i++) {
      for (
        let j = 0;
        $selectedStep + 1 < $websiteArray.length &&
        j < $websiteArray[$selectedStep + 1].length;
        j++
      ) {
        try {
          let index1 =
            $websiteIndexArray[$selectedStep][$currentSelectedNodeIds[i][3]];
          let index2 = j;
          let linkInsideRectId = `linkRectInside${$selectedStep}${index1}${index2}`;
          let linkOutsideRectId = `linkRectOutside${$selectedStep}${index1}${index2}`;
          if (!afterSelectedSavedInsideLink.includes(linkInsideRectId)) {
            let linkInsideRect = document.getElementById(linkInsideRectId);
            linkInsideRect.setAttribute("opacity", "0.2");
            opacityIds.update((values) => [...values, linkInsideRectId]);
          }
          if (!afterSelectedSavedOutsideLink.includes(linkOutsideRectId)) {
            let linkOutsideRect = document.getElementById(linkOutsideRectId);
            linkOutsideRect.setAttribute("opacity", "0.2");
            opacityIds.update((values) => [...values, linkOutsideRectId]);
          }
        } catch (error) {
          continue;
        }
      }
    }
  }
  // 筛选条件函数
  function ifSavedPath(everyArray) {
    let isSaved = false;
    for (let i = 0; i < $currentSelectedNodeIds.length; i++) {
      if (everyArray[$selectedStep] == $currentSelectedNodeIds[i][3]) {
        isSaved = true;
        break;
      }
    }
    return isSaved;
  }
  //根据选择的节点筛选路径
  function filterPath() {
    filterFlow1.update((data) => {
      let origindata = [...data];
      return origindata.filter((everyArray) => ifSavedPath(everyArray));
    });
    filterFlow2.update((data) => {
      let origindata = [...data];
      return origindata.filter((everyArray) => ifSavedPath(everyArray));
    });
    console.log("filterFlow1:", $filterFlow1);
    console.log("filterFlow2:", $filterFlow2);
    nextStepSavdeNode = [];
    for (let i = 0; i < $filterFlow1.length; i++) {
      try {
        if (!nextStepSavdeNode.includes($filterFlow1[i][$selectedStep + 1])) {
          nextStepSavdeNode.push($filterFlow1[i][$selectedStep + 1]);
        }
      } catch (error) {
        break;
      }
    }
    for (let i = 0; i < $filterFlow2.length; i++) {
      try {
        if (!nextStepSavdeNode.includes($filterFlow2[i][$selectedStep + 1])) {
          nextStepSavdeNode.push($filterFlow2[i][$selectedStep + 1]);
        }
      } catch (error) {
        break;
      }
    }
    console.log("下一步可以被选中的节点:", nextStepSavdeNode);
    //选中后，只保留存在路径的link，其他的都虚化
    afterSelectedSavedInsideLink = [];
    afterSelectedSavedOutsideLink = [];
    for (let i = 0; i < $filterFlow1.length; i++) {
      try {
        let source =
          $websiteIndexArray[$selectedStep][$filterFlow1[i][$selectedStep]];
        let target =
          $websiteIndexArray[$selectedStep + 1][
            $filterFlow1[i][$selectedStep + 1]
          ];
        if (
          !afterSelectedSavedInsideLink.includes(
            `linkRectInside${$selectedStep}${source}${target}`
          )
        ) {
          afterSelectedSavedInsideLink.push(
            `linkRectInside${$selectedStep}${source}${target}`
          );
        }
        if (
          !afterSelectedSavedOutsideLink.includes(
            `linkRectOutside${$selectedStep}${source}${target}`
          )
        ) {
          afterSelectedSavedOutsideLink.push(
            `linkRectOutside${$selectedStep}${source}${target}`
          );
        }
      } catch (error) {}
    }
    for (let i = 0; i < $filterFlow2.length; i++) {
      try {
        let source =
          $websiteIndexArray[$selectedStep][$filterFlow2[i][$selectedStep]];
        let target =
          $websiteIndexArray[$selectedStep + 1][
            $filterFlow2[i][$selectedStep + 1]
          ];
        if (
          !afterSelectedSavedInsideLink.includes(
            `linkRectInside${$selectedStep}${source}${target}`
          )
        ) {
          afterSelectedSavedInsideLink.push(
            `linkRectInside${$selectedStep}${source}${target}`
          );
        }
        if (
          !afterSelectedSavedOutsideLink.includes(
            `linkRectOutside${$selectedStep}${source}${target}`
          )
        ) {
          afterSelectedSavedOutsideLink.push(
            `linkRectOutside${$selectedStep}${source}${target}`
          );
        }
      } catch (error) {}
    }
    console.log("保留的外部link:", afterSelectedSavedOutsideLink);
    console.log("保留的内部link:", afterSelectedSavedInsideLink);
  }
  //画路径
  export function drawPath() {
    const svgContainer = document.getElementById("svg-container");
    const SVG_NS = "http://www.w3.org/2000/svg"; // 创建一个SVG namespace
    for (let i = 0; i < $filterFlow1.length; i++) {
      try {
        let path = $filterFlow1[i];
        let fromName = path[$selectedStep - 1];
        let toName = path[$selectedStep];
        let fromNo = $websiteIndexArray[$selectedStep - 1][fromName];
        let toNo = $websiteIndexArray[$selectedStep][toName];
        let line1 = document.createElementNS(SVG_NS, "line");
        line1.setAttribute(
          "x1",
          `${$pathPositionOfNode[$selectedStep - 1][fromNo].fromX}`
        );
        line1.setAttribute(
          "y1",
          `${$pathPositionOfNode[$selectedStep - 1][fromNo].fromY}`
        );
        line1.setAttribute(
          "x2",
          `${$pathPositionOfLink[$selectedStep - 1][fromNo][toNo].toX}`
        );
        line1.setAttribute(
          "y2",
          `${$pathPositionOfLink[$selectedStep - 1][fromNo][toNo].toY}`
        );
        line1.setAttribute("stroke", "blue");
        line1.setAttribute("stroke-width", "2");
        line1.setAttribute("transform", `translate(0, 300) rotate(-45)`);
        let line2 = document.createElementNS(SVG_NS, "line");
        line2.setAttribute(
          "x1",
          `${$pathPositionOfLink[$selectedStep - 1][fromNo][toNo].fromX}`
        );
        line2.setAttribute(
          "y1",
          `${$pathPositionOfLink[$selectedStep - 1][fromNo][toNo].fromY}`
        );
        line2.setAttribute(
          "x2",
          `${$pathPositionOfNode[$selectedStep][toNo].toX}`
        );
        line2.setAttribute(
          "y2",
          `${$pathPositionOfNode[$selectedStep][toNo].toY}`
        );
        line2.setAttribute("stroke", "blue");
        line2.setAttribute("stroke-width", "2");
        line2.setAttribute("transform", `translate(0, 300) rotate(-45)`);
        svgContainer.appendChild(line1);
        svgContainer.appendChild(line2);
      } catch (error) {
        continue;
      }
    }
    for (let i = 0; i < $filterFlow2.length; i++) {
      try {
        let path = $filterFlow2[i];
        let fromName = path[$selectedStep - 1];
        let toName = path[$selectedStep];
        let fromNo = $websiteIndexArray[$selectedStep - 1][fromName];
        let toNo = $websiteIndexArray[$selectedStep][toName];
        let line1 = document.createElementNS(SVG_NS, "line");
        line1.setAttribute(
          "x1",
          `${$pathPositionOfNode[$selectedStep - 1][fromNo].fromX}`
        );
        line1.setAttribute(
          "y1",
          `${$pathPositionOfNode[$selectedStep - 1][fromNo].fromY}`
        );
        line1.setAttribute(
          "x2",
          `${$pathPositionOfLink[$selectedStep - 1][fromNo][toNo].toX}`
        );
        line1.setAttribute(
          "y2",
          `${$pathPositionOfLink[$selectedStep - 1][fromNo][toNo].toY}`
        );
        line1.setAttribute("stroke", "blue");
        line1.setAttribute("stroke-width", "2");
        line1.setAttribute("transform", `translate(0, 300) rotate(-45)`);
        let line2 = document.createElementNS(SVG_NS, "line");
        line2.setAttribute(
          "x1",
          `${$pathPositionOfLink[$selectedStep - 1][fromNo][toNo].fromX}`
        );
        line2.setAttribute(
          "y1",
          `${$pathPositionOfLink[$selectedStep - 1][fromNo][toNo].fromY}`
        );
        line2.setAttribute(
          "x2",
          `${$pathPositionOfNode[$selectedStep][toNo].toX}`
        );
        line2.setAttribute(
          "y2",
          `${$pathPositionOfNode[$selectedStep][toNo].toY}`
        );
        line2.setAttribute("stroke", "blue");
        line2.setAttribute("stroke-width", "2");
        line2.setAttribute("transform", `translate(0, 300) rotate(-45)`);
        svgContainer.appendChild(line1);
        svgContainer.appendChild(line2);
      } catch (error) {
        continue;
      }
    }
  }
  //响应式更新showpath
  $: if ($selectedRectNumber != 0) {
    showPath.set(true);
    console.log("showPath:", $showPath);
  } else {
    showPath.set(false);
    console.log("showPath:", $showPath);
  }
  export { updateSelectedStep, resetSelectedStep };
</script>
