<script>
  import Node from "./components/Node.svelte";
  import Link from "./components/Link.svelte";
  import Website from "./components/website.svelte";
  import ShowPath from "./components/ShowPath.svelte";
  import {
    selectedNodeIds,
    selectedRectNumber,
    selectedStep,
    showPath,
    websiteArray,
    ifSelected,
    currentSelectedNodeIds,
    opacityIds,
    clickFlow1,
    clickFlow2,
    filterFlow1,
    filterFlow2,
    websiteIndexArray,
    maxLinkVolumn,
    pathPositionOfLink,
    pathPositionOfNode,
  } from "./store";

  ///////////////////////////////////////////////////////////////////////////////////////////////////////
  let selectedOption1;
  // 数据选项
  let options1 = [
    { id: 1, name: "选项1" },
    { id: 2, name: "选项2" },
    { id: 3, name: "选项3" },
  ];
  let selectedOption2;
  // 数据选项
  let options2 = [
    { id: 1, name: "选项1" },
    { id: 2, name: "选项2" },
    { id: 3, name: "选项3" },
  ];
  ///////////////////////////////////////////////////////////////////////////////////////////////////////
  let cellSize = 15; //方格大小
  //node属性
  let nodePositionX = 50;
  let nodePositionY = 50;
  let nodeArray = [
    [
      [30, 30],
      [30, 30],
      [30, 30],
      [30, 30],
      [30, 30],
    ],
    [
      [30, 30],
      [30, 30],
      [30, 30],
      [30, 30],
      [30, 30],
    ],
    [
      [30, 30],
      [30, 30],
      [30, 30],
      [30, 30],
      [30, 30],
    ],
    [
      [30, 30],
      [30, 30],
      [30, 30],
      [30, 30],
      [30, 30],
    ],
  ];
  let maxLength = 50;
  let nodeAttributesArray = [];
  //Link链接方格属性
  let linkPositionX = nodePositionX + maxLength;
  let linkPositionY = nodePositionY;
  let volumnArray = [
    [
      [
        [10, 10],
        [10, 10],
        [10, 10],
        [5, 5],
        [7, 7],
      ],
      [
        [1, 1],
        [4, 4],
        [6, 6],
        [6, 6],
        [5, 5],
      ],
      [
        [7, 7],
        [9, 9],
        [10, 10],
        [3, 3],
        [5, 5],
      ],
      [
        [3, 3],
        [9, 9],
        [8, 8],
        [5, 5],
        [5, 5],
      ],
      [
        [10, 10],
        [5, 5],
        [8, 8],
        [5, 5],
        [6, 6],
      ],
    ],
    [
      [
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
      ],
      [
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
      ],
      [
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
      ],
      [
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
      ],
      [
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
      ],
    ],
    [
      [
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
      ],
      [
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
      ],
      [
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
      ],
      [
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
      ],
      [
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
        [10, 10],
      ],
    ],
  ];
  let linkAttributesArray = [];
  //website属性
  let radius = cellSize / 2;
  let websiteNameArray = [
    ["A", "B", "C", "D", "E"],
    ["A", "B", "C", "D", "E"],
    ["A", "B", "C", "D", "E"],
    ["A", "B", "C", "D", "E"],
  ];
  let websiteAttributesArray = [];
  //获取所有node,link,website的属性
  function getAttributes() {
    //获取node属性
    for (let i = 0; i < nodeArray.length; i++) {
      let nodeAmounts = nodeArray[i].length;
      let nodeAttributes = {
        stepNumber: i,
        positionX: nodePositionX,
        positionY: nodePositionY,
        cellSize: cellSize,
        length: nodeArray[i],
        maxLength: maxLength,
        pageName: websiteNameArray[i],
        nextNodeSize:
          i + 1 < websiteNameArray.length ? websiteNameArray[i + 1].length : 0,
      };
      nodeAttributesArray.push(nodeAttributes);
      if (i % 2 == 0) {
        nodePositionX = nodePositionX + maxLength;
        nodePositionY = nodePositionY + nodeAmounts * cellSize;
      } else {
        nodePositionY = nodePositionY + maxLength;
        nodePositionX = nodePositionX + nodeAmounts * cellSize;
      }
    }
    //获取link属性
    for (let i = 0; i < volumnArray.length; i++) {
      let linkAttributes = {
        cellSize: cellSize,
        positionX: linkPositionX,
        positionY: linkPositionY,
        volumn: volumnArray[i],
        stepNumber: i,
      };
      linkAttributesArray.push(linkAttributes);
      if (i < volumnArray.length - 1) {
        if (i % 2 == 0) {
          linkPositionY = nodeAttributesArray[i + 2].positionY;
        } else {
          linkPositionX = nodeAttributesArray[i + 2].positionX;
        }
      }
    }
    //获取website属性
    let websitePositionX =
      nodeAttributesArray[0].positionX +
      maxLength +
      cellSize * nodeArray[1].length;
    let websitePositionY = nodeAttributesArray[0].positionY;
    for (let i = 0; i < websiteNameArray.length; i++) {
      let websiteAttributes = {
        stepNumber: i,
        radius: radius,
        websiteName: websiteNameArray[i],
        positionX: websitePositionX,
        positionY: websitePositionY,
      };
      websiteAttributesArray.push(websiteAttributes);
      if (i <= websiteNameArray.length - 2) {
        if (i == websiteNameArray.length - 2) {
          if (i % 2 == 0) {
            websitePositionX = nodeAttributesArray[i + 1].positionX;
            websitePositionY =
              nodeAttributesArray[i].positionY +
              nodeArray[i].length * cellSize +
              maxLength;
          } else {
            websitePositionY = nodeAttributesArray[i + 1].positionY;
            websitePositionX =
              nodeAttributesArray[i].positionX +
              nodeArray[i].length * cellSize +
              maxLength;
          }
        } else {
          if (i % 2 == 0) {
            websitePositionX = nodeAttributesArray[i + 1].positionX;
            websitePositionY =
              nodeAttributesArray[i].positionY +
              (nodeArray[i].length + nodeArray[i + 2].length) * cellSize +
              maxLength;
          } else {
            websitePositionY = nodeAttributesArray[i + 1].positionY;
            websitePositionX =
              nodeAttributesArray[i].positionX +
              (nodeArray[i].length + nodeArray[i + 2].length) * cellSize +
              maxLength;
          }
        }
      }
    }
  }

  //从后端取数据
  async function fetchdata() {
    const response = await fetch(`http://127.0.0.1:5000`);
    const data = await response.json();
    console.log(data);
    return data;
  }
  // 点击获取数据集
  async function getDataSets() {
    let data = await fetchdata();
    websiteNameArray = data["网站名称"];
    maxLinkVolumn.set(data["最大link流量"]);
    let nv = data["node流量"];
    let nvv = [];
    for (let i of nv) {
      let nvvv = [];
      // console.log(i);
      for (let j in i) {
        // console.log(i[j]["node_clicks"]);
        nvvv.push(i[j]["node_clicks"]);
      }
      nvv.push(nvvv);
    }
    let websiteIndexs = [];
    for (let i of nv) {
      let websiteIndex = {};
      for (let j in i) {
        websiteIndex[j] = i[j]["index"];
      }
      websiteIndexs.push(websiteIndex);
    }
    websiteIndexArray.set(websiteIndexs);
    console.log("网站每一步的索引值:", $websiteIndexArray);
    nodeArray = nvv;
    console.log(nodeArray.length);
    volumnArray = data["matrix流量"];
    clickFlow1.set(data["click_flow1"]);
    clickFlow2.set(data["click_flow2"]);
    filterFlow1.set(data["click_flow1"]);
    filterFlow2.set(data["click_flow2"]);
    // console.log("click_flow1:", $clickFlow1);
    // console.log("click_flow2:", $clickFlow2);
    updateAttributes();
    //更新store
    showPath.set(false); //定义是否进入选择并显示路径的模式
    selectedRectNumber.set(0); //被选中的矩形节点个数
    selectedStep.set(0); //选择进行到的步骤序号
    selectedNodeIds.set([]); //保存所有被选中的节点id
    ifSelected.set([]); //保存节点是否被选中的状态
    currentSelectedNodeIds.set([]); //保存当前step选中的节点id
    opacityIds.set([]);
    pathPositionOfLink.set({});
    pathPositionOfNode.set({});
  }

  // 更新属性
  function updateAttributes() {
    //初始化
    nodePositionX = 50;
    nodePositionY = 50;
    linkPositionX = nodePositionX + maxLength;
    linkPositionY = nodePositionY;
    let newNodeAttributesArray = [];
    let newLinkAttributesArray = [];
    let newWebsiteAttributesArray = [];
    //获取node属性
    for (let i = 0; i < nodeArray.length; i++) {
      let nodeAmounts = nodeArray[i].length;
      let nodeAttributes = {
        stepNumber: i,
        positionX: nodePositionX,
        positionY: nodePositionY,
        cellSize: cellSize,
        length: nodeArray[i],
        maxLength: maxLength,
        pageName: websiteNameArray[i],
        nextNodeSize:
          i + 1 < websiteNameArray.length ? websiteNameArray[i + 1].length : 0,
      };
      newNodeAttributesArray.push(nodeAttributes);
      if (i % 2 == 0) {
        nodePositionX = nodePositionX + maxLength;
        nodePositionY = nodePositionY + nodeAmounts * cellSize;
      } else {
        nodePositionY = nodePositionY + maxLength;
        nodePositionX = nodePositionX + nodeAmounts * cellSize;
      }
    }
    //获取link属性
    for (let i = 0; i < volumnArray.length; i++) {
      let linkAttributes = {
        cellSize: cellSize,
        positionX: linkPositionX,
        positionY: linkPositionY,
        volumn: volumnArray[i],
        stepNumber: i,
      };
      newLinkAttributesArray.push(linkAttributes);
      if (i < volumnArray.length - 1) {
        if (i % 2 == 0) {
          linkPositionY = newNodeAttributesArray[i + 2].positionY;
        } else {
          linkPositionX = newNodeAttributesArray[i + 2].positionX;
        }
      }
    }
    //获取website属性
    let websitePositionX =
      newNodeAttributesArray[0].positionX +
      maxLength +
      cellSize * nodeArray[1].length;
    let websitePositionY = newNodeAttributesArray[0].positionY;
    for (let i = 0; i < websiteNameArray.length; i++) {
      let websiteAttributes = {
        stepNumber: i,
        radius: radius,
        websiteName: websiteNameArray[i],
        positionX: websitePositionX,
        positionY: websitePositionY,
      };
      newWebsiteAttributesArray.push(websiteAttributes);
      if (i <= websiteNameArray.length - 2) {
        if (i == websiteNameArray.length - 2) {
          if (i % 2 == 0) {
            websitePositionX = newNodeAttributesArray[i + 1].positionX;
            websitePositionY =
              newNodeAttributesArray[i].positionY +
              nodeArray[i].length * cellSize +
              maxLength;
          } else {
            websitePositionY = newNodeAttributesArray[i + 1].positionY;
            websitePositionX =
              newNodeAttributesArray[i].positionX +
              nodeArray[i].length * cellSize +
              maxLength;
          }
        } else {
          if (i % 2 == 0) {
            websitePositionX = newNodeAttributesArray[i + 1].positionX;
            websitePositionY =
              newNodeAttributesArray[i].positionY +
              (nodeArray[i].length + nodeArray[i + 2].length) * cellSize +
              maxLength;
          } else {
            websitePositionY = newNodeAttributesArray[i + 1].positionY;
            websitePositionX =
              newNodeAttributesArray[i].positionX +
              (nodeArray[i].length + nodeArray[i + 2].length) * cellSize +
              maxLength;
          }
        }
      }
    }
    //完成最后的属性更新
    nodeAttributesArray = newNodeAttributesArray;
    linkAttributesArray = newLinkAttributesArray;
    websiteAttributesArray = newWebsiteAttributesArray;
  }
  let showPathEntity; //showpath绑定实例
  //初始化matrixwave
  getAttributes();
  $: {
    websiteArray.set(websiteNameArray);
    console.log("websiteArray:", $websiteArray);
  }
  // onMount(() => {
  //   const svg = document.getElementById("svg-container");
  //   let zoom = 1;
  //   let panX = 0;
  //   let panY = 0;

  //   let isDragging = false;
  //   let startX = 0;
  //   let startY = 0;

  //   svg.addEventListener("wheel", function (event) {
  //     event.preventDefault();
  //     const scaleFactor = 0.1;
  //     if (event.deltaY < 0) {
  //       zoom += scaleFactor;
  //     } else {
  //       zoom -= scaleFactor;
  //     }
  //     // 避免过度缩小
  //     zoom = Math.max(zoom, 0.1);
  //     svg.setAttribute(
  //       "viewBox",
  //       `${panX} ${panY} ${800 / zoom} ${600 / zoom}`
  //     );
  //   });
  //   svg.addEventListener("mousedown", function (event) {
  //     isDragging = true;
  //     startX = event.clientX;
  //     startY = event.clientY;
  //   });
  //   svg.addEventListener("mousemove", function (event) {
  //     if (!isDragging) return;
  //     let dx = event.clientX - startX;
  //     let dy = event.clientY - startY;
  //     startX = event.clientX;
  //     startY = event.clientY;
  //     panX -= dx / zoom;
  //     panY -= dy / zoom;
  //     svg.setAttribute(
  //       "viewBox",
  //       `${panX} ${panY} ${800 / zoom} ${600 / zoom}`
  //     );
  //   });
  //   svg.addEventListener("mouseup", function (event) {
  //     isDragging = false;
  //   });
  //   svg.addEventListener("mouseleave", function (event) {
  //     isDragging = false;
  //   });
  // });
</script>

<div class="container">
  <div class="option">
    <!-- 功能区 -->
    <h1>Dataset</h1>
    <!-- <br/> -->
    <div class="dataset">
      <select bind:value={selectedOption1}>
        {#each options1 as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      <select bind:value={selectedOption2}>
        {#each options2 as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      <button on:click={getDataSets}>获取数据集</button>
    </div>
    <h1>ShowPath</h1>
    <div class="show-path">
      {#if $showPath != false}
        <button on:click={showPathEntity.updateSelectedStep}>next step</button>
        <button on:click={showPathEntity.resetSelectedStep}>reset</button>
      {/if}
    </div>
  </div>
  <div class="matrixwave">
    <svg
      id="svg-container"
      width="100%"
      height="100%"
      style="overflow: visible;"
      preserveAspectRatio="xMidYMid meet"
    >
      <g transform="translate(0, 300) rotate(-45)">
        {#each nodeAttributesArray as item (item)}
          <Node
            stepNumber={item.stepNumber}
            positionX={item.positionX}
            positionY={item.positionY}
            cellSize={item.cellSize}
            length={item.length}
            maxLength={item.maxLength}
            pageName={item.pageName}
            nextNodeSize={item.nextNodeSize}
          />
        {/each}
        {#each linkAttributesArray as item (item)}
          <Link
            cellSize={item.cellSize}
            positionX={item.positionX}
            positionY={item.positionY}
            volumn={item.volumn}
            stepNumber={item.stepNumber}
          />
        {/each}
        {#each websiteAttributesArray as item, i (item)}
          <Website
            stepNumber={i}
            {radius}
            websiteName={item.websiteName}
            positionX={item.positionX}
            positionY={item.positionY}
          />
        {/each}
      </g>
      <ShowPath bind:this={showPathEntity} />
    </svg>
  </div>
</div>

<style>
  h1 {
    /* 调整字号大小 */
    font-size: 3em;
    /* 将标题居中 */
    text-align: center;
  }
  .dataset {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  .show-path {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  select {
    width: 80%;
    height: 50px;
    border-radius: 5px;
    border: 1px solid #ccc;
    padding: 5px;
    font-size: 16px;
  }
  button {
    background-color: #63e2f0; /* Green */
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    transition-duration: 0.4s;
    border-radius: 12px;
  }

  button:hover {
    background-color: white;
    color: black;
    border: 2px solid #63e2f0;
  }
  .container {
    display: flex;
    flex-direction: row;
    width: 100%;
    height: 100%;
  }

  .option {
    flex: 1;
    background-color: antiquewhite;
  }

  .matrixwave {
    flex: 5;
    /* background-color: brown; */
  }
</style>
