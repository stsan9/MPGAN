import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep

plt.switch_backend("agg")
plt.rcParams.update({"font.size": 16})
plt.style.use(hep.style.CMS)


def _real_gen_hists(real_data, gen_data, bins, label, parts=True):
    plt.ticklabel_format(axis="y", scilimits=(0, 0), useMathText=True)
    _ = plt.hist(real_data, bins=bins, histtype="step", label="Real", color="red")
    _ = plt.hist(gen_data, bins=bins, histtype="step", label="Generated", color="blue")
    plt.xlabel(label)
    plt.ylabel(f"Number of {'Particles' if parts else 'Jets'}")
    plt.legend(loc=1, prop={"size": 18})


def plot_part_feats(
    jet_type,
    real_jets,
    gen_jets,
    real_mask=None,
    gen_mask=None,
    coords="polarrel",
    name=None,
    figs_path=None,
    dataset="jetnet",
    num_particles=30,
    losses=None,
    const_ylim=False,
    show=False,
):
    """Plot particle feature histograms"""
    if coords == "cartesian":
        plabels = ["$p_x$ (GeV)", "$p_y$ (GeV)", "$p_z$ (GeV)"]
        bin = np.arange(-500, 500, 10)
        pbins = [bin, bin, bin]
    elif coords == "polarrel":
        if dataset == "jetnet":
            plabels = ["$\eta^{rel}$", "$\phi^{rel}$", "$p_T^{rel}$"]
            if jet_type == "g" or jet_type == "q" or jet_type == "w" or jet_type == "z":
                if num_particles == 100:
                    pbins = [
                        np.arange(-0.5, 0.5, 0.005),
                        np.arange(-0.5, 0.5, 0.005),
                        np.arange(0, 0.1, 0.001),
                    ]
                else:
                    pbins = [
                        np.linspace(-0.3, 0.3, 100),
                        np.linspace(-0.3, 0.3, 100),
                        np.linspace(0, 0.2, 100),
                    ]
                    ylims = [3e5, 3e5, 3e5]
            elif jet_type == "t":
                pbins = [
                    np.linspace(-0.5, 0.5, 100),
                    np.linspace(-0.5, 0.5, 100),
                    np.linspace(0, 0.2, 100),
                ]
        elif dataset == "jets-lagan":
            plabels = ["$\eta^{rel}$", "$\phi^{rel}$", "$p_T^{rel}$"]
            pbins = [
                np.linspace(-1.25, 1.25, 25 + 1),
                np.linspace(-1.25, 1.25, 25 + 1),
                np.linspace(0, 1, 51),
            ]
    elif coords == "polarrelabspt":
        plabels = ["$\eta^{rel}$", "$\phi^{rel}$", "$p_T (GeV)$"]
        pbins = [
            np.linspace(-0.5, 0.5, 100),
            np.linspace(-0.5, 0.5, 100),
            np.linspace(0, 200, 100),
        ]

    if real_mask is not None:
        parts_real = real_jets[real_mask]
        parts_gen = gen_jets[gen_mask]
    else:
        parts_real = real_jets.reshape(-1, real_jets.shape[2])
        parts_gen = gen_jets.reshape(-1, gen_jets.shape[2])

    fig = plt.figure(figsize=(22, 8))

    for i in range(3):
        fig.add_subplot(1, 3, i + 1)
        plt.ticklabel_format(axis="y", scilimits=(0, 0), useMathText=True)
        _ = plt.hist(parts_real[:, i], pbins[i], histtype="step", label="Real", color="red")
        _ = plt.hist(parts_gen[:, i], pbins[i], histtype="step", label="Generated", color="blue")
        plt.xlabel("Particle " + plabels[i])
        plt.ylabel("Number of Particles")
        if const_ylim:
            plt.ylim(0, ylims[i])
        if losses is not None and "w1p" in losses:
            plt.title(
                f'$W_1$ = {losses["w1p"][-1][i]:.2e} ± {losses["w1p"][-1][i + len(losses["w1p"][-1]) // 2]:.2e}',
                fontsize=12,
            )
        plt.legend(loc=1, prop={"size": 18})

    plt.tight_layout(pad=2.0)
    if figs_path is not None and name is not None:
        plt.savefig(figs_path + name + ".pdf", bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()


def plot_part_feats_jet_mass(
    jet_type,
    real_jets,
    gen_jets,
    real_mask,
    gen_mask,
    real_masses,
    gen_masses,
    num_particles=30,
    coords="polarrel",
    name=None,
    figs_path=None,
    dataset="jetnet",
    losses=None,
    const_ylim=False,
    show=False,
):
    """Plot histograms of particle feature + jet mass in one row"""
    if coords == "cartesian":
        plabels = ["$p_x$ (GeV)", "$p_y$ (GeV)", "$p_z$ (GeV)"]
        bin = np.arange(-500, 500, 10)
        pbins = [bin, bin, bin]
    elif coords == "polarrel":
        plabels = ["$\eta^{rel}$", "$\phi^{rel}$", "$p_T^{rel}$"]
        if jet_type == "g" or jet_type == "q" or jet_type == "w" or jet_type == "z":
            if num_particles == 100:
                pbins = [
                    np.arange(-0.5, 0.5, 0.005),
                    np.arange(-0.5, 0.5, 0.005),
                    np.arange(0, 0.1, 0.001),
                ]
            else:
                pbins = [
                    np.linspace(-0.3, 0.3, 100),
                    np.linspace(-0.3, 0.3, 100),
                    np.linspace(0, 0.2, 100),
                ]
        elif jet_type == "t":
            pbins = [
                np.linspace(-0.5, 0.5, 100),
                np.linspace(-0.5, 0.5, 100),
                np.linspace(0, 0.2, 100),
            ]

        mlabel = "Jet $m/p_{T}$"
    elif coords == "polarrelabspt":
        plabels = ["$\eta^{rel}$", "$\phi^{rel}$", "$p_T (GeV)$"]
        pbins = [
            np.linspace(-0.5, 0.5, 100),
            np.linspace(-0.5, 0.5, 100),
            np.linspace(0, 1500, 100),
        ]

        mlabel = "Jet m (GeV)"

    if jet_type == "g" or jet_type == "q" or jet_type == "t":
        mbins = np.linspace(0, 0.225, 51)
    else:
        mbins = np.linspace(0, 0.12, 51)

    if real_mask is not None:
        parts_real = real_jets[real_mask]
        parts_gen = gen_jets[gen_mask]
    else:
        parts_real = real_jets.reshape(-1, real_jets.shape[2])
        parts_gen = gen_jets.reshape(-1, gen_jets.shape[2])

    fig = plt.figure(figsize=(30, 8))

    for i in range(3):
        fig.add_subplot(1, 4, i + 1)
        plt.ticklabel_format(axis="y", scilimits=(0, 0), useMathText=True)
        _ = plt.hist(parts_real[:, i], pbins[i], histtype="step", label="Real", color="red")
        _ = plt.hist(parts_gen[:, i], pbins[i], histtype="step", label="Generated", color="blue")
        plt.xlabel("Particle " + plabels[i])
        plt.ylabel("Number of Particles")
        if losses is not None and "w1p" in losses:
            plt.title(
                f'$W_1$ = {losses["w1p"][-1][i]:.2e} ± {losses["w1p"][-1][i + len(losses["w1p"][-1]) // 2]:.2e}',
                fontsize=12,
            )

        plt.legend(loc=1, prop={"size": 18})

    fig.add_subplot(1, 4, 4)
    plt.ticklabel_format(axis="y", scilimits=(0, 0), useMathText=True)
    _ = plt.hist(real_masses, bins=mbins, histtype="step", label="Real", color="red")
    _ = plt.hist(gen_masses, bins=mbins, histtype="step", label="Generated", color="blue")
    plt.xlabel(mlabel)
    plt.ylabel("Jets")
    plt.legend(loc=1, prop={"size": 18})
    if losses is not None and "w1m" in losses:
        plt.title(f'$W_1$ = {losses["w1m"][-1][0]:.2e} ± {losses["w1m"][-1][1]:.2e}', fontsize=12)

    plt.tight_layout(pad=2.0)
    if figs_path is not None and name is not None:
        plt.savefig(figs_path + name + ".pdf", bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()


def plot_jet_feats(
    jet_type,
    real_masses,
    gen_masses,
    real_efps,
    gen_efps,
    coords="polarrel",
    name=None,
    figs_path=None,
    losses=None,
    show=False,
):
    """Plot 5 EFPs and jet mass histograms"""

    if coords == "polarrel":
        if jet_type == "g":
            binranges = [0.0013, 0.0004, 0.0004, 0.0004, 0.0004]
        elif jet_type == "q":
            binranges = [0.002, 0.001, 0.001, 0.0005, 0.0005]
        else:
            binranges = [0.0045, 0.0035, 0.004, 0.002, 0.003]

        if jet_type == "g" or jet_type == "q" or jet_type == "t":
            mbins = np.linspace(0, 0.225, 51)
        else:
            mbins = np.linspace(0, 0.12, 51)

        mlabel = "Jet $m/p_{T}$"
    elif coords == "polarrelabspt":
        if jet_type == "g":
            binranges = [4e10, 1e10, 1e10, 1e10, 1e10]
        elif jet_type == "q":
            binranges = [0.002, 0.001, 0.001, 0.0005, 0.0005]
        else:
            binranges = [0.0045, 0.0035, 0.004, 0.002, 0.003]

        if jet_type == "g" or jet_type == "q" or jet_type == "t":
            mbins = np.linspace(0, 500, 50)
        else:
            mbins = np.linspace(0, 0.12, 51)

        mlabel = "Jet m (GeV)"

    bins = [np.linspace(0, binr, 100) for binr in binranges]

    fig = plt.figure(figsize=(20, 12))

    fig.add_subplot(2, 3, 1)
    plt.ticklabel_format(axis="y", scilimits=(0, 0), useMathText=True)
    _ = plt.hist(real_masses, bins=mbins, histtype="step", label="Real", color="red")
    _ = plt.hist(gen_masses, bins=mbins, histtype="step", label="Generated", color="blue")
    plt.xlabel(mlabel)
    plt.ylabel("Jets")
    plt.legend(loc=1, prop={"size": 18})

    if losses is not None and "w1m" in losses:
        plt.title(f'$W_1$ = {losses["w1m"][-1][0]:.2e} ± {losses["w1m"][-1][1]:.2e}', fontsize=12)

    for i in range(5):
        fig.add_subplot(2, 3, i + 2)
        plt.ticklabel_format(axis="y", scilimits=(0, 0), useMathText=True)
        plt.ticklabel_format(axis="x", scilimits=(0, 0), useMathText=True)
        _ = plt.hist(real_efps[:, i], bins[i], histtype="step", label="Real", color="red")
        _ = plt.hist(gen_efps[:, i], bins[i], histtype="step", label="Generated", color="blue")
        plt.xlabel("EFP " + str(i + 1), x=0.7)
        plt.ylabel("Jets")
        plt.legend(loc=1, prop={"size": 18})
        if losses is not None and "w1efp" in losses:
            plt.title(
                f'$W_1$ = {losses["w1efp"][-1][i]:.2e} ± {losses["w1efp"][-1][i + len(losses["w1efp"][-1]) // 2]:.2e}',
                fontsize=12,
            )

    plt.tight_layout(pad=0.5)
    if figs_path is not None and name is not None:
        plt.savefig(figs_path + name + ".pdf", bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()


def plot_jet_mass_pt(
    jet_type,
    real_masses,
    gen_masses,
    real_pts,
    gen_pts,
    coords="polarrel",
    name=None,
    figs_path=None,
    losses=None,
    show=False,
):
    if coords == "polarrel":
        mlabel = "Jet $m/p_{T}$"
        ptlabel = "Jet Relative $p_T$"
        mbins = np.linspace(0, 0.225, 101)
        ptbins = np.linspace(0.5, 1.2, 101)
    elif coords == "polarrelabspt":
        mlabel = "Jet m (GeV)"
        ptlabel = "Jet $p_T$ (GeV)"
        mbins = np.linspace(0, 500, 101)
        ptbins = np.linspace(0, 4000, 101)

    fig = plt.figure(figsize=(16, 8))

    fig.add_subplot(1, 2, 1)
    _real_gen_hists(real_masses, gen_masses, mbins, mlabel, parts=False)

    fig.add_subplot(1, 2, 2)
    _real_gen_hists(real_pts, gen_pts, ptbins, ptlabel, parts=False)

    plt.tight_layout(pad=2)
    if figs_path is not None and name is not None:
        plt.savefig(figs_path + name + ".pdf", bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()


def plot_losses(losses, loss="lg", name=None, losses_path=None, show=False):
    """Plot loss curves"""
    plt.figure()

    if loss == "og" or loss == "ls":
        plt.plot(losses["Dr"], label="Discriminitive real loss")
        plt.plot(losses["Df"], label="Discriminitive fake loss")
        plt.plot(losses["G"], label="Generative loss")
    elif loss == "w":
        plt.plot(losses["D"], label="Critic loss")
    elif loss == "hinge":
        plt.plot(losses["Dr"], label="Discriminitive real loss")
        plt.plot(losses["Df"], label="Discriminitive fake loss")
        plt.plot(losses["G"], label="Generative loss")

    if "gp" in losses:
        plt.plot(losses["gp"], label="Gradient penalty")

    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()

    if losses_path is not None and name is not None:
        plt.savefig(losses_path + name + ".pdf", bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()


def plot_eval(
    losses, epoch, save_epochs, coords="polarrel", name=None, losses_path=None, show=False
):
    """Evaluation metric plots per epoch"""
    if coords == "cartesian":
        plabels = ["$p_x$ (GeV)", "$p_y$ (GeV)", "$p_z$ (GeV)"]
    elif coords == "polarrel":
        plabels = ["$\eta^{rel}$", "$\phi^{rel}$", "$p_T^{rel}$"]
    elif coords == "polarrelabspt":
        plabels = ["$\eta^{rel}$", "$\phi^{rel}$", "$p_T (GeV)$"]
    # jlabels = ['Relative Mass', 'Relative $p_T$', 'EFP']
    colors = ["blue", "green", "orange", "red", "yellow"]

    x = np.arange(0, epoch + 1, save_epochs)[-len(losses["w1p"]) :]

    fig = plt.figure(figsize=(30, 24))

    if "w1p" in losses:
        for i in range(3):
            fig.add_subplot(3, 3, i + 1)
            plt.plot(x, np.array(losses["w1p"])[:, i])
            plt.xlabel("Epoch")
            plt.ylabel("Particle " + plabels[i] + " $W_1$")
            plt.yscale("log")

    # x = np.arange(0, epoch + 1, args.save_epochs)[-len(losses['w1j_' + str(args.w1_num_samples[0]) + 'm']):]

    if "w1m" in losses:
        fig.add_subplot(3, 3, 4)
        plt.plot(x, np.array(losses["w1m"])[:, 0])
        plt.xlabel("Epoch")
        plt.ylabel("Jet Relative Mass $W_1$")
        plt.yscale("log")

    if "w1efp" in losses:
        fig.add_subplot(3, 3, 5)
        for i in range(5):
            plt.plot(x, np.array(losses["w1p"])[:, i], label="EFP " + str(i + 1), color=colors[i])
        plt.legend(loc=1)
        plt.xlabel("Epoch")
        plt.ylabel("Jet EFPs $W_1$")
        plt.yscale("log")

    if "mmd" in losses and "coverage" in losses:
        # x = x[-len(losses['mmd']):]
        metrics = {"mmd": (1, "MMD"), "coverage": (2, "Coverage")}
        for key, (i, label) in metrics.items():
            fig.add_subplot(3, 3, 6 + i)
            plt.plot(x, np.array(losses[key]))
            plt.xlabel("Epoch")
            plt.ylabel(label)
            if key == "mmd":
                plt.yscale("log")

    if "fpnd" in losses:
        fig.add_subplot(3, 3, 9)
        plt.plot(x, np.array(losses["fpnd"]))
        plt.xlabel("Epoch")
        plt.ylabel("FPND")
        plt.yscale("log")

    if losses_path is not None and name is not None:
        plt.savefig(losses_path + name + ".pdf", bbox_inches="tight")

    if show:
        plt.show()
    else:
        plt.close()
