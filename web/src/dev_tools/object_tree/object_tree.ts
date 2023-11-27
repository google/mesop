import { FlatTreeControl } from "@angular/cdk/tree";
import { Component, Input } from "@angular/core";
import {
  MatTreeFlatDataSource,
  MatTreeFlattener,
  MatTreeModule,
} from "@angular/material/tree";
import { CdkTreeModule } from "@angular/cdk/tree";
import { MatIconModule } from "@angular/material/icon";
import { MatButtonModule } from "@angular/material/button";

/** Flat node with expandable and level information */
interface ExampleFlatNode {
  expandable: boolean;
  name: string;
  value: string;
  level: number;
  duration: number | undefined;
}

@Component({
  selector: "optic-object-tree",
  templateUrl: "object_tree.ng.html",
  styleUrl: "object_tree.css",
  standalone: true,
  imports: [CdkTreeModule, MatTreeModule, MatButtonModule, MatIconModule],
})
export class ObjectTree {
  @Input({ required: true }) object: object;

  keys() {
    return Object.keys(this.object);
  }
  private _transformer = (node: PropertyNode, level: number) => {
    return {
      expandable: !!node.children && node.children.length > 0,
      name: node.key,
      value: node.value,
      level: level,
      duration: node.duration,
    };
  };

  treeControl = new FlatTreeControl<ExampleFlatNode>(
    (node) => node.level,
    (node) => node.expandable,
  );

  treeFlattener = new MatTreeFlattener(
    this._transformer,
    (node) => node.level,
    (node) => node.expandable,
    (node) => node.children,
  );

  dataSource = new MatTreeFlatDataSource(this.treeControl, this.treeFlattener);

  ngOnInit() {
    this.dataSource.data = mapObject(this.object);

    this.treeControl.dataNodes.forEach((node) => {
      if (node.level < 2) {
        this.treeControl.expand(node);
      }
    });
  }

  hasChild = (_: number, node: ExampleFlatNode) => node.expandable;
}

function mapObject(object: object): PropertyNode[] {
  const nodes: PropertyNode[] = [];
  for (const key of Object.keys(object)) {
    // Skip showing duration & timestamp since we have special handling for them.
    if (key === "duration" || key === "timestamp") {
      continue;
    }
    const value = (object as any)[key];
    const node: PropertyNode = {
      key,
      value: JSON.stringify(value),
    };
    const duration = (object as any)["duration"];
    if (node.key === "type" && duration) {
      node.duration = duration;
    }
    if (typeof value === "object" && value !== null) {
      node.children = mapObject(value);
    }
    if (value || node.children) {
      nodes.push(node);
    }
  }
  return nodes;
}

interface PropertyNode {
  key: string;
  value: string;
  children?: PropertyNode[];
  duration?: number;
}
