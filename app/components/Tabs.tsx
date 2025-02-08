import { useState } from "react";

const Tabs = () => {
  const [activeTab, setActiveTab] = useState<string>("tab1");

  const isActive = (tab: string) => activeTab === tab;

  const tabs: { id: string; label: string }[] = [
    { id: "tab1", label: "グラフ" },
    { id: "tab2", label: "遷移図" },
    { id: "tab3", label: "式変形" },
    { id: "tab4", label: "イメージ生成" },
  ];

  return (
    <div className="w-1/3">
      <div className="text-sm font-medium text-center text-gray-400 border-b border-gray-200 dark:text-gray-400 dark:border-slate-700">
        <ul className="flex flex-wrap -mb-px">
          {tabs.map((tab) => (
            <li key={tab.id} className="mr-2 cursor-pointer">
              <a
                onClick={() => setActiveTab(tab.id)}
                className={`inline-block p-4 rounded-t-lg border-b-2 border-transparent ${
                  isActive(tab.id)
                    ? "text--600 green border-blue-600"
                    : "hover:text-slate-600 hover:border-gray-300 dark:hover:text-gray-300"
                }`}
              >
                {tab.label}
              </a>
            </li>
          ))}
        </ul>
      </div>
      
      <div className="p-4">
        {tabs.map((tab) => (
          <div key={tab.id} className={isActive(tab.id) ? "block" : "hidden"}>
            <span className="font-semibold">何を作りたいか</span> : ここにプロット例を記載します。
          </div>
        ))}
      </div>
    </div>
  );
};

export default Tabs;
