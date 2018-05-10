package org.opt4j.optimizers.ea.aeseh;

/**
 * The {@link EpsilonAdaptationDefault} adapts the ε values exactly as described
 * in the paper cited in the {@link AeSeHModule}.
 * 
 * @author Fedor Smirnov
 *
 */
public class EpsilonAdaptationDefault implements EpsilonAdaptation {

	@Override
	public void adaptEpsilon(AdaptiveEpsilon adaptiveEpsilon, boolean epsilonTooBig) {
		if (epsilonTooBig) {
			adaptiveEpsilon.setEpsilon(adaptiveEpsilon.getEpsilon() - adaptiveEpsilon.getEpsilonDelta());
			adaptiveEpsilon.setEpsilonDelta(adaptiveEpsilon.getEpsilonDelta() / 2);
		} else {
			adaptiveEpsilon.setEpsilon(adaptiveEpsilon.getEpsilon() + adaptiveEpsilon.getEpsilonDelta());
			adaptiveEpsilon.setEpsilonDelta(adaptiveEpsilon.getEpsilonDelta() * 2);
		}
	}
}
