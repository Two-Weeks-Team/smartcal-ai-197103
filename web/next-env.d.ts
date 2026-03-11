/// <reference types="next" />
/// <reference types="next/types/global" />
/// <reference types="next/image-types" />

declare module "@/components/*" {
  const component: any;
  export default component;
}

declare module "@/app/*" {
  const component: any;
  export default component;
}

declare module "@/lib/*" {
  const value: any;
  export default value;
}