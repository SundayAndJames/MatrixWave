<script>
  import { maxLinkVolumn, pathPositionOfLink } from "../store";
  export let cellSize = 15;
  export let positionX = 100;
  export let positionY = 50;
  export let stepNumber = 0;
  export let volumn = [
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
  ];
  let length1 = volumn.length * cellSize;
  let length2 = volumn[0].length * cellSize;
  let insideRectMaxSide = 0.8 * cellSize;
  let pathPosition = [];
  if (stepNumber % 2 == 0) {
    for (let i = 0; i < volumn.length; i++) {
      let temp = [];
      for (let j = 0; j < volumn[i].length; j++) {
        let toX = positionX + cellSize * j;
        let toY = positionY + cellSize / 2 + cellSize * i;
        let fromX = positionX + cellSize / 2 + cellSize * j;
        let fromY = positionY + cellSize + cellSize * i;
        temp.push({ toX: toX, toY: toY, fromX: fromX, fromY: fromY });
      }
      pathPosition.push(temp);
    }
  } else {
    for (let i = 0; i < volumn.length; i++) {
      let temp = [];
      for (let j = 0; j < volumn[i].length; j++) {
        let toX = positionX + cellSize / 2 + cellSize * i;
        let toY = positionY + cellSize * j;
        let fromX = positionX + cellSize + cellSize * i;
        let fromY = positionY + cellSize / 2 + cellSize * j;
        temp.push({ toX: toX, toY: toY, fromX: fromX, fromY: fromY });
      }
      pathPosition.push(temp);
    }
  }
  pathPositionOfLink.update((values) => {
    return { ...values, [stepNumber]: pathPosition };
  });
  //用于画虚线的长度
  function getInterpolatedColor(p, o) {
    const white = { r: 255, g: 255, b: 255 };
    const orange = { r: 255, g: 165, b: 0 };
    const purple = { r: 204, g: 153, b: 255 };
    if (p >= o) {
      let t = (p - o) / (p + o);
      const r = Math.round(white.r + t * (purple.r - white.r));
      const g = Math.round(white.g + t * (purple.g - white.g));
      const b = Math.round(white.b + t * (purple.b - white.b));
      return `rgb(${r}, ${g}, ${b})`;
    } else {
      let t = (o - p) / (p + o);
      const r = Math.round(white.r + t * (orange.r - white.r));
      const g = Math.round(white.g + t * (orange.g - white.g));
      const b = Math.round(white.b + t * (orange.b - white.b));
      return `rgb(${r}, ${g}, ${b})`;
    }
  }
  //悬停
  //mouseover link_rect
  function mouseoverLinkRect(i, j) {
    //悬停处link矩形框变红
    let linkRect = document.getElementById(
      `linkRectOutside${stepNumber}${i}${j}`
    );
    linkRect.style.stroke = "red";
    linkRect.style.strokeWidth = "2";
    //突出显示源节点和目标节点
    let nodeRect1 = document.getElementById(`nodeRect${i}${stepNumber}`);
    let nodeRect2 = document.getElementById(`nodeRect${j}${stepNumber + 1}`);
    if (nodeRect1.style.stroke !== "blue") {
      nodeRect1.style.stroke = "red";
      nodeRect1.style.strokeWidth = "2";
    }
    if (nodeRect2.style.stroke !== "blue") {
      nodeRect2.style.stroke = "red";
      nodeRect2.style.strokeWidth = "2";
    }
  }
  //mouseleave link_rect
  function mouseleaveLinkRect(i, j) {
    //恢复矩形框为黑色
    let linkRect = document.getElementById(
      `linkRectOutside${stepNumber}${i}${j}`
    );
    linkRect.style.stroke = "#fff";
    linkRect.style.strokeWidth = "1";
    //恢复源节点和目标节点
    let nodeRect1 = document.getElementById(`nodeRect${i}${stepNumber}`);
    let nodeRect2 = document.getElementById(`nodeRect${j}${stepNumber + 1}`);
    if (nodeRect1.style.stroke !== "blue") {
      nodeRect1.style.stroke = "black";
      nodeRect1.style.strokeWidth = "1";
    }
    if (nodeRect2.style.stroke !== "blue") {
      nodeRect2.style.stroke = "black";
      nodeRect2.style.strokeWidth = "1";
    }
  }
</script>

<!-- 构造矩阵 -->
{#each volumn as item1, i}
  {#each item1 as item2, j}
    {#if item2[0] != 0 || item2[1] != 0}
      {#if stepNumber % 2 == 0}
        <!-- 外部矩形 -->
        <rect
          class="linkRect"
          id="linkRectOutside{stepNumber}{i}{j}"
          x={j * cellSize + positionX}
          y={i * cellSize + positionY}
          width={cellSize}
          height={cellSize}
          style="stroke: #fff; fill: {getInterpolatedColor(
            item2[0],
            item2[1]
          )};stroke-width: 1;"
          on:mouseenter={() => mouseoverLinkRect(i, j)}
          on:mouseleave={() => mouseleaveLinkRect(i, j)}
        />
        <!-- 内部矩形 -->
        <rect
          id="linkRectInside{stepNumber}{i}{j}"
          x={j * cellSize +
            positionX +
            cellSize / 2 -
            (((item2[0] + item2[1]) / 2 / $maxLinkVolumn) * insideRectMaxSide) /
              2}
          y={i * cellSize +
            positionY +
            cellSize / 2 -
            (((item2[0] + item2[1]) / 2 / $maxLinkVolumn) * insideRectMaxSide) /
              2}
          width={((item2[0] + item2[1]) / 2 / $maxLinkVolumn) *
            insideRectMaxSide}
          height={((item2[0] + item2[1]) / 2 / $maxLinkVolumn) *
            insideRectMaxSide}
          style="fill: #000;"
          on:mouseenter={() => mouseoverLinkRect(i, j)}
          on:mouseleave={() => mouseleaveLinkRect(i, j)}
        />
      {:else}
        <!-- 外部矩形 -->
        <rect
          class="linkRect"
          id="linkRectOutside{stepNumber}{i}{j}"
          x={i * cellSize + positionX}
          y={j * cellSize + positionY}
          width={cellSize}
          height={cellSize}
          style="stroke: #fff; fill: {getInterpolatedColor(
            item2[0],
            item2[1]
          )};stroke-width: 1"
          on:mouseenter={() => mouseoverLinkRect(i, j)}
          on:mouseleave={() => mouseleaveLinkRect(i, j)}
        />
        <!-- 内部矩形 -->
        <rect
          id="linkRectInside{stepNumber}{i}{j}"
          x={i * cellSize +
            positionX +
            cellSize / 2 -
            (((item2[0] + item2[1]) / 2 / $maxLinkVolumn) * insideRectMaxSide) /
              2}
          y={j * cellSize +
            positionY +
            cellSize / 2 -
            (((item2[0] + item2[1]) / 2 / $maxLinkVolumn) * insideRectMaxSide) /
              2}
          width={((item2[0] + item2[1]) / 2 / $maxLinkVolumn) *
            insideRectMaxSide}
          height={((item2[0] + item2[1]) / 2 / $maxLinkVolumn) *
            insideRectMaxSide}
          style="fill: #000;"
          on:mouseenter={() => mouseoverLinkRect(i, j)}
          on:mouseleave={() => mouseleaveLinkRect(i, j)}
        />
      {/if}
    {/if}
  {/each}
{/each}
<!-- 添加虚线框和实线框 -->
{#if stepNumber % 2 == 0}
  <line
    x1={positionX}
    y1={positionY}
    x2={positionX + length2}
    y2={positionY}
    stroke="black"
    stroke-width="1"
    stroke-dasharray="5,5"
  />
  <line
    x1={positionX}
    y1={positionY}
    x2={positionX}
    y2={positionY + length1}
    stroke="black"
    stroke-width="1"
    stroke-dasharray="5,5"
  />
  <line
    x1={positionX + length2}
    y1={positionY + length1}
    x2={positionX}
    y2={positionY + length1}
    stroke="black"
    stroke-width="1"
    stroke-dasharray="5,5"
  />
  <line
    x1={positionX + length2}
    y1={positionY + length1}
    x2={positionX + length2}
    y2={positionY}
    stroke="black"
    stroke-width="1"
    stroke-dasharray="5,5"
  />
  <line
    x1={positionX + length2 - cellSize}
    y1={positionY}
    x2={positionX + length2 - cellSize}
    y2={positionY + length1}
    stroke="black"
    stroke-width="1"
  />
{:else}
  <line
    x1={positionX}
    y1={positionY}
    x2={positionX}
    y2={positionY + length2}
    stroke="black"
    stroke-width="1"
    stroke-dasharray="5,5"
  />
  <line
    x1={positionX}
    y1={positionY}
    x2={positionX + length1}
    y2={positionY}
    stroke="black"
    stroke-width="1"
    stroke-dasharray="5,5"
  />
  <line
    x1={positionX + length1}
    y1={positionY + length2}
    x2={positionX + length1}
    y2={positionY}
    stroke="black"
    stroke-width="1"
    stroke-dasharray="5,5"
  />
  <line
    x1={positionX + length2}
    y1={positionY + length2}
    x2={positionX}
    y2={positionY + length2}
    stroke="black"
    stroke-width="1"
    stroke-dasharray="5,5"
  />
  <line
    x1={positionX}
    y1={positionY + length2 - cellSize}
    x2={positionX + length1}
    y2={positionY + length2 - cellSize}
    stroke="black"
    stroke-width="1"
  />
{/if}
