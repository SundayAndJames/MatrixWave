<script>
  import Node from "./Node.svelte";
  import Link from "./Link.svelte";
  import Website from "./website.svelte";
  let cellSize = 15; //方格大小
  //node属性
  let nodePositionX = 50;
  let nodePositionY = 50;
  let nodeArray = [
    [30, 30, 30, 30, 30],
    [30, 30, 30, 30, 30],
    [30, 30, 30, 30, 30],
    [30, 30, 30, 30, 30],
  ];
  let maxLength = 50;
  let nodeAttributesArray = [];
  //Link链接方格属性
  let linkPositionX = nodePositionX + maxLength;
  let linkPositionY = nodePositionY;
  let volumnArray = [
    [
      [10, 10, 10, 5, 7],
      [1, 4, 6, 6, 5],
      [7, 9, 10, 3, 5],
      [3, 9, 8, 5, 5],
      [10, 5, 8, 5, 6],
    ],
    [
      [10, 10, 10, 10, 10],
      [10, 10, 10, 10, 10],
      [10, 10, 10, 10, 10],
      [10, 10, 10, 10, 10],
      [10, 10, 10, 10, 10],
    ],
    [
      [10, 10, 10, 10, 10],
      [10, 10, 10, 10, 10],
      [10, 10, 10, 10, 10],
      [10, 10, 10, 10, 10],
      [10, 10, 10, 10, 10],
    ],
  ];
  let linkAttributesArray = [];
  //website属性

  let radius = cellSize / 2;
  let websiteNameArray = [
    ["myweb.com", "youtube.com", "hunan.com", "zhejiang.com", "jiangxi.com"],
    ["myweb.com", "youtube.com", "hunan.com", "zhejiang.com", "jiangxi.com"],
    ["myweb.com", "youtube.com", "hunan.com", "zhejiang.com", "jiangxi.com"],
    ["myweb.com", "youtube.com", "hunan.com", "zhejiang.com", "jiangxi.com"],
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
  getAttributes();
</script>

<div>
  <svg width="100%" height="100%" style="overflow: visible;">
    {#each nodeAttributesArray as item}
      <Node
        stepNumber={item.stepNumber}
        positionX={item.positionX}
        positionY={item.positionY}
        cellSize={item.cellSize}
        length={item.length}
        maxLength={item.maxLength}
      />
    {/each}
    {#each linkAttributesArray as item}
      <Link
        cellSize={item.cellSize}
        positionX={item.positionX}
        positionY={item.positionY}
        volumn={item.volumn}
      />
    {/each}
    {#each websiteAttributesArray as item, i}
      <Website
        stepNumber={i}
        {radius}
        websiteName={item.websiteName}
        positionX={item.positionX}
        positionY={item.positionY}
      />
    {/each}
  </svg>
</div>
