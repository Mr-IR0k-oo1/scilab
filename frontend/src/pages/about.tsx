import SubPage from './SubPage';

export default function AboutPage() {
  return (
    <SubPage title="About FOSSEE">
      <p>
        FOSSEE (Free and Open Source Software in Education) is an initiative by IIT Bombay to promote
        the use of open source software in education. The project aims to reduce the dependency on
        proprietary software in academic institutions by providing viable open source alternatives.
      </p>

      <h2 className="text-base font-bold mt-8 mb-3">Our Mission</h2>
      <p>
        To make quality engineering tools accessible to every student and educator in India.
        We believe that no student should be limited by software licensing costs, and no educator
        should have to build their curriculum around proprietary tools.
      </p>

      <h2 className="text-base font-bold mt-8 mb-3">The Team</h2>
      <p>
        Backed by the Indian Institute of Technology Bombay, FOSSEE is developed by a team of
        researchers, engineers, and educators who are passionate about open source and education.
        The project is funded by the National Mission on Education through Information and
        Communication Technology (NMEICT).
      </p>

      <div className="grid md:grid-cols-3 gap-px bg-border mt-8">
        {[
          { val: '100+', label: 'University Partners' },
          { val: '500K+', label: 'Students Reached' },
          { val: '2000+', label: 'Lab Installations' },
        ].map((s) => (
          <div key={s.label} className="bg-card p-6 text-center">
            <p className="text-2xl font-bold text-primary">{s.val}</p>
            <p className="text-xs text-muted-foreground/70 mt-1">{s.label}</p>
          </div>
        ))}
      </div>
    </SubPage>
  );
}
