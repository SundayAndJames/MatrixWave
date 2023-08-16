<script>
  import {
    selectedRectNumber,
    selectedStep,
    ifSelected,
    currentSelectedNodeIds,
    websiteArray,
    pathPositionOfNode,
  } from "../store";
  import { onMount } from "svelte";
  export let stepNumber = 0;
  export let positionX = 50;
  export let positionY = 50;
  export let cellSize = 15; //方格大小
  export let length = [
    [35, 35],
    [45, 45],
    [40, 40],
    [30, 30],
    [50, 50],
  ];
  export let pageName = ["A", "B", "C", "D", "E"];
  export let maxLength = 50;
  export let nextNodeSize = 0;
  let pathPosition = [];
  if (stepNumber % 2 == 0) {
    for (let i = 0; i < pageName.length; i++) {
      let toX = positionX;
      let toY = positionY + cellSize / 2 + cellSize * i;
      let fromX = positionX + maxLength;
      let fromY = toY;
      pathPosition.push({ fromX: fromX, fromY: fromY, toX: toX, toY: toY });
    }
  } else {
    for (let i = 0; i < pageName.length; i++) {
      let toX = positionX + cellSize / 2 + cellSize * i;
      let toY = positionY;
      let fromX = toX;
      let fromY = positionY + maxLength;
      pathPosition.push({ fromX: fromX, fromY: fromY, toX: toX, toY: toY });
    }
  }
  pathPositionOfNode.update((values) => {
    return { ...values, [stepNumber]: pathPosition };
  });
  ////////////////////////////////////////////////////////////////////////////////////
  //操控悬浮label
  function handleMouseEnter(i) {
    const SVG_NS = "http://www.w3.org/2000/svg"; // 创建一个SVG namespace
    let rect = document.createElementNS(SVG_NS, "rect");
    const svgContainer = document.getElementById("svg-container");
    let textElement1 = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "text"
    );
    let textElement2 = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "text"
    );
    //设置rect属性
    rect.setAttributeNS(null, "class", "label");
    rect.setAttributeNS(null, "width", "200");
    rect.setAttributeNS(null, "height", "50");
    rect.setAttributeNS(null, "fill", "rgba(200,200,200,0.8)");
    rect.setAttributeNS(null, "stroke", "black");
    rect.setAttributeNS(null, "rx", "5");
    rect.setAttributeNS(null, "ry", "5");
    //设置text属性
    textElement1.textContent = `Page: ${pageName[i]}`;
    textElement2.textContent = `Vistors: ${length[i][0]}, ${length[i][1]} (${
      length[i][0] >= length[i][1] ? "-" : "+"
    }${Math.abs(((length[i][0] - length[i][1]) / length[i][0]) * 100).toFixed(
      2
    )}%)`;
    if (stepNumber % 2 == 0) {
      let x = positionX + maxLength / 2 - (length[i][0] + length[i][1]) / 2 / 2;
      let y = positionY + i * cellSize + cellSize;
      rect.setAttributeNS(null, "y", `${y}`);
      rect.setAttributeNS(null, "x", `${x}`);
      textElement1.setAttribute("x", `${x}`); // x坐标
      textElement1.setAttribute("y", `${y}`); // y坐标
      textElement2.setAttribute("x", `${x}`); // x坐标
      textElement2.setAttribute("y", `${y}`); // y坐标
    } else {
      let x = positionX + i * cellSize;
      let y =
        positionY +
        maxLength / 2 -
        (length[i][0] + length[i][1]) / 2 / 2 +
        (length[i][0] + length[i][1]) / 2;
      rect.setAttributeNS(null, "y", `${y} `);
      rect.setAttributeNS(null, "x", `${x}`);
      textElement1.setAttribute("x", `${x}`); // x坐标
      textElement1.setAttribute("y", `${y}`); // y坐标
      textElement2.setAttribute("x", `${x}`); // x坐标
      textElement2.setAttribute("y", `${y}`); // y坐标
    }
    let x = rect.getAttribute("x");
    let y = rect.getAttribute("y");
    rect.setAttributeNS(
      null,
      "transform",
      `translate(0, 300) rotate(-45) rotate(45 ${x} ${y})`
    );
    textElement1.setAttribute("font-family", "Arial"); // 字体
    textElement1.setAttribute("font-size", "16px"); // 字体大小
    textElement1.setAttribute("class", "text"); // 字体大小
    textElement1.setAttribute("dx", "5px");
    textElement1.setAttribute("dy", "18px");
    textElement1.setAttribute(
      "transform",
      `translate(0, 300) rotate(-45) rotate(45 ${x} ${y})`
    );
    textElement2.setAttribute("font-family", "Arial"); // 字体
    textElement2.setAttribute("font-size", "16px"); // 字体大小
    textElement2.setAttribute("class", "text"); // 字体大小
    textElement2.setAttribute("dx", "5px");
    textElement2.setAttribute("dy", "38px");
    textElement2.setAttribute(
      "transform",
      `translate(0, 300) rotate(-45) rotate(45 ${x} ${y})`
    );
    // 将rect附加到SVG容器
    svgContainer.appendChild(rect);
    svgContainer.appendChild(textElement1);
    svgContainer.appendChild(textElement2);

    //将节点边框变红
    let rectNodes = document.querySelectorAll(`rect.${pageName[i]}`);
    rectNodes.forEach((node) => {
      // @ts-ignore
      if (node.style.stroke !== "blue") {
        // @ts-ignore
        node.style.stroke = "red";
        // @ts-ignore
        node.style.strokeWidth = "2px";
      }
    });

    //网站名称变红
    let websitePages = document.querySelectorAll(`text.${pageName[i]}`);
    websitePages.forEach((page) => {
      // @ts-ignore
      page.style.fill = "red";
    });
    //矩阵中节点对应的列用红色线包围
    let line1 = document.createElementNS(SVG_NS, "line");
    let line2 = document.createElementNS(SVG_NS, "line");
    let line3 = document.createElementNS(SVG_NS, "line");
    let line4 = document.createElementNS(SVG_NS, "line");
    let x1, x2, x3, x4, y1, y2, y3, y4;
    if (stepNumber % 2 == 0) {
      x1 = positionX + maxLength;
      y1 = positionY + cellSize * i;
      x2 = x1 + nextNodeSize * cellSize;
      y2 = y1;
      x3 = x1;
      y3 = y2 + cellSize;
      x4 = x2;
      y4 = y3;
    } else {
      x1 = positionX + cellSize * i;
      y1 = positionY + maxLength;
      x2 = x1;
      y2 = y1 + cellSize * nextNodeSize;
      x3 = x1 + cellSize;
      y3 = y1;
      x4 = x3;
      y4 = y2;
    }
    //line1属性
    line1.setAttribute("x1", `${x1}`);
    line1.setAttribute("y1", `${y1}`);
    line1.setAttribute("x2", `${x2}`);
    line1.setAttribute("y2", `${y2}`);
    line1.setAttribute("class", "highlightline");
    line1.setAttribute("stroke", "red");
    line1.setAttribute("stroke-width", "2");
    line1.setAttribute("transform", `translate(0, 300) rotate(-45)`);
    //line2属性
    line2.setAttribute("x1", `${x1}`);
    line2.setAttribute("y1", `${y1}`);
    line2.setAttribute("x2", `${x3}`);
    line2.setAttribute("y2", `${y3}`);
    line2.setAttribute("class", "highlightline");
    line2.setAttribute("stroke", "red");
    line2.setAttribute("stroke-width", "2");
    line2.setAttribute("transform", `translate(0, 300) rotate(-45)`);
    //line3属性
    line3.setAttribute("x1", `${x3}`);
    line3.setAttribute("y1", `${y3}`);
    line3.setAttribute("x2", `${x4}`);
    line3.setAttribute("y2", `${y4}`);
    line3.setAttribute("class", "highlightline");
    line3.setAttribute("stroke", "red");
    line3.setAttribute("stroke-width", "2");
    line3.setAttribute("transform", `translate(0, 300) rotate(-45)`);
    //line4属性
    line4.setAttribute("x1", `${x2}`);
    line4.setAttribute("y1", `${y2}`);
    line4.setAttribute("x2", `${x4}`);
    line4.setAttribute("y2", `${y4}`);
    line4.setAttribute("class", "highlightline");
    line4.setAttribute("stroke", "red");
    line4.setAttribute("stroke-width", "2");
    line4.setAttribute("transform", `translate(0, 300) rotate(-45)`);
    svgContainer.appendChild(line1);
    svgContainer.appendChild(line2);
    svgContainer.appendChild(line3);
    svgContainer.appendChild(line4);
  }

  function handleMouseLeave(i) {
    // 选择具有类名'label1'的所有矩形
    let labelRects = document.querySelectorAll(".label");
    let texts = document.querySelectorAll(".text");
    // 遍历选择的矩形，并从其父节点中删除它们
    labelRects.forEach((rect) => {
      rect.parentNode.removeChild(rect);
    });
    texts.forEach((text) => {
      text.parentNode.removeChild(text);
    });

    //恢复节点边框为黑色
    let rectNodes = document.querySelectorAll(`rect.${pageName[i]}`);
    rectNodes.forEach((node) => {
      // @ts-ignore
      if (node.style.stroke !== "blue") {
        // @ts-ignore
        node.style.stroke = "black";
        // @ts-ignore
        node.style.strokeWidth = "1px";
      }
    });

    //网站名称恢复黑色
    let websitePages = document.querySelectorAll(`text.${pageName[i]}`);
    websitePages.forEach((page) => {
      // @ts-ignore
      page.style.fill = "black";
    });
    //删除矩阵中红色线框
    let highlightlines = document.querySelectorAll(".highlightline");
    highlightlines.forEach((line) => {
      line.parentNode.removeChild(line);
    });
  }
  ////////////////////////////////////////////////////////////////////////////////////
  //颜色函数
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
  ////////////////////////////////////////////////////////////////////////////////////
  //选中节点
  function click2Select(event, i) {
    let rectElement = event.target;
    if (
      stepNumber == $selectedStep &&
      (rectElement.getAttribute("opacity") == "1" ||
        rectElement.getAttribute("opacity") == null)
    ) {
      ifSelected.update((values) => {
        values[stepNumber][i] = !values[stepNumber][i];
        return values;
      });
      //被选中
      if ($ifSelected[stepNumber][i]) {
        $selectedRectNumber += 1; //选中个数+1
        //更新currentSelectedNodeIds
        currentSelectedNodeIds.update((value) => {
          return [
            ...value,
            [
              `nodeRect${i}${stepNumber}`,
              stepNumber,
              i,
              $websiteArray[stepNumber][i],
            ],
          ];
        });
        let rectNodes = document.querySelectorAll(`rect.${pageName[i]}`);
        rectNodes.forEach((node) => {
          // @ts-ignore
          if (node.style.stroke !== "blue") {
            // @ts-ignore
            node.style.stroke = "black";
            // @ts-ignore
            node.style.strokeWidth = "1px";
          }
        });
        rectElement.style.stroke = "blue";
        rectElement.style.strokeWidth = "2px";
      }
      //不被选中
      else {
        $selectedRectNumber -= 1;
        //更新currentSelectedNodeIds
        currentSelectedNodeIds.update((data) => {
          return data.filter(
            (item) =>
              !arraysAreEqual(item, [
                `nodeRect${i}${stepNumber}`,
                stepNumber,
                i,
                $websiteArray[stepNumber][i],
              ])
          );
        });
        let rectNodes = document.querySelectorAll(`rect.${pageName[i]}`);
        rectNodes.forEach((node) => {
          // @ts-ignore
          if (node.style.stroke !== "blue") {
            // @ts-ignore
            node.style.stroke = "black";
            // @ts-ignore
            node.style.strokeWidth = "1px";
          }
        });
        rectElement.style.stroke = "black";
        rectElement.style.strokeWidth = "1px";
      }
      console.log("selectedRectNumber:", $selectedRectNumber);
      console.log("currentSelectedNodeIds:", $currentSelectedNodeIds);
    }
  }
  function arraysAreEqual(a, b) {
    return a.length === b.length && a.every((val, index) => val === b[index]);
  }
  onMount(() => {
    ifSelected.update((data) => {
      let addedArray = new Array(pageName.length).fill(false);
      return [...data, addedArray];
    });
  });
</script>

{#each length as item, i}
  {#if stepNumber % 2 == 0}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <rect
      class={pageName[i]}
      id="nodeRect{i}{stepNumber}"
      x={positionX + maxLength / 2 - (item[0] + item[1]) / 2 / 2}
      y={positionY + i * cellSize}
      width={(item[0] + item[1]) / 2}
      height={cellSize}
      style="stroke: #000; fill: {getInterpolatedColor(item[0], item[1])};"
      on:mouseenter={() => handleMouseEnter(i)}
      on:mouseleave={() => handleMouseLeave(i)}
      on:click={() => click2Select(event, i)}
    />
  {:else}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <rect
      class={pageName[i]}
      id="nodeRect{i}{stepNumber}"
      y={positionY + maxLength / 2 - (item[0] + item[1]) / 2 / 2}
      x={positionX + i * cellSize}
      height={(item[0] + item[1]) / 2}
      width={cellSize}
      style="stroke: #000; fill: {getInterpolatedColor(item[0], item[1])};"
      on:mouseenter={() => handleMouseEnter(i)}
      on:mouseleave={() => handleMouseLeave(i)}
      on:click={() => click2Select(event, i)}
    />
  {/if}
{/each}
