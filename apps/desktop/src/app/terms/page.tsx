import SubPage from '@/components/SubPage';

export default function TermsPage() {
  return (
    <SubPage title="Terms of Use">
      <p>
        By using FOSSEE tools and the Open Engineering Workspace, you agree to these terms.
        FOSSEE is provided as free and open source software, governed by its respective licenses.
      </p>

      <h2 className="text-base font-bold mt-8 mb-3">Software License</h2>
      <p>
        All FOSSEE tools are released under open source licenses. Scilab is distributed under the
        CeCILL license, compatible with the GNU GPL. Xcos, eSim, and OpenModelica are distributed
        under their respective open source licenses. You are free to use, modify, and distribute
        the software in accordance with these licenses.
      </p>

      <h2 className="text-base font-bold mt-8 mb-3">Disclaimer</h2>
      <p>
        FOSSEE tools are provided &ldquo;as is&rdquo; without warranty of any kind. The project
        maintainers and IIT Bombay are not liable for any damages arising from the use of these tools.
        Users are responsible for validating the accuracy of simulation results.
      </p>

      <h2 className="text-base font-bold mt-8 mb-3">Contributions</h2>
      <p>
        Contributions to FOSSEE projects are welcome and encouraged. By contributing code,
        documentation, or examples, you agree to license your contributions under the same
        open source license as the project you are contributing to.
      </p>
    </SubPage>
  );
}
