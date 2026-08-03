import SubPage from './SubPage';

export default function PrivacyPage() {
  return (
    <SubPage title="Privacy Policy">
      <p>
        FOSSEE respects your privacy. This policy outlines how we collect, use, and protect your
        information when you use our platform and tools.
      </p>

      <h2 className="text-base font-bold mt-8 mb-3">Information We Collect</h2>
      <p>
        We collect minimal information necessary to provide our services. This includes project
        metadata, usage statistics, and optional feedback submissions. We do not collect personal
        information unless voluntarily provided.
      </p>

      <h2 className="text-base font-bold mt-8 mb-3">How We Use Your Data</h2>
      <p>
        Usage data helps us improve the platform and understand how educators and students interact
        with FOSSEE tools. We do not sell, share, or monetize your data. All project files remain
        on your local machine unless you explicitly choose to share them.
      </p>

      <h2 className="text-base font-bold mt-8 mb-3">Open Source</h2>
      <p>
        All FOSSEE tools are fully open source. You can inspect, modify, and audit the source code
        at any time. Transparency is a core principle of our project.
      </p>
    </SubPage>
  );
}
